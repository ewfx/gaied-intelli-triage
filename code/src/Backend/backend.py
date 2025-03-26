import base64
import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_together import ChatTogether # Updated import
from dotenv import load_dotenv
import os
import utils
from pdf2image import convert_from_bytes
import io
import email
from email import policy

load_dotenv()

REQUEST_TYPES = {
    "Adjustment": [],
    "AU Transfer": [],
    "Closing Notice": ["Reallocation Fees", "Amendment Fees", "Reallocation Principal"],
    "Commitment Change": ["Cashless Roll", "Decrease", "Increase"],
    "Fee Payment": ["Ongoing Fee", "Letter of Credit Fee"],
    "Money Movement-Inbound": ["Principal", "Interest", "Principal + Interest", "Principal + Interest + Fee"],
    "Money Movement-Outbound": ["Timebound", "Foreign Currency"]
}

FIELD_MAPPING = {
    "Adjustment": ["Deal Name", "Amount", "Effective Date", "Sender", "Receiver"],
    "Money Movement-Inbound": ["Deal Name", "Amount", "Bank Name", "ABA Number", "Account Number", "Reference", "Sender", "Receiver"],
    "AU Transfer": ["Deal Name", "Bank Name", "ABA Number", "Account Number", "Sender", "Receiver"],
    "Closing Notice": ["Deal Name", "Amount", "Effective Date", "Sender", "Receiver"],
    "Commitment Change": ["Deal Name", "Amount", "Effective Date", "Sender", "Receiver"],
    "Fee Payment": ["Deal Name", "Amount", "Bank Name", "ABA Number", "Account Number", "Sender", "Receiver"],
    "Money Movement-Outbound": ["Deal Name", "Amount", "Bank Name", "ABA Number", "Account Number", "Sender", "Receiver"]
}

def perform_ocr(document):
    """Perform OCR using Together AI"""
    try:
        if hasattr(document, 'seek'):
            document.seek(0)
        model = ChatTogether(model="meta-llama/Llama-Vision-Free")
        img = base64.b64encode(document.read()).decode('utf-8')
        sys_msg = SystemMessage(content="Extract all text from the image accurately.")
        human_msg = HumanMessage(content=[
            {"type": "text", "text": "Return raw text only, no formatting."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img}"}},
        ])
        response = model.invoke([sys_msg, human_msg])
        print(f"DEBUG: OCR Response = '{response.content}'")
        return response.content.strip()
    except Exception as e:
        print(f"ERROR: OCR Failed - {str(e)}")
        return f"OCR Error: {str(e)}"

def parse_eml(file):
    """Parse .eml file to extract email body and attachments"""
    file.seek(0)
    msg = email.message_from_bytes(file.read(), policy=policy.default)
    email_body = ""
    attachment_texts = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" and not part.get_filename():
                email_body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
            elif content_type == "application/pdf":
                pdf_data = part.get_payload(decode=True)
                images = convert_from_bytes(pdf_data, dpi=200)
                for img in images:
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    img_byte_arr.seek(0)
                    text = perform_ocr(img_byte_arr)
                    attachment_texts.append(text)
    else:
        email_body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

    return email_body.strip(), attachment_texts

def classify_request(email_body, attachment_texts):
    """Classify requests using Together AI"""
    model = ChatTogether(model="meta-llama/Llama-Vision-Free")
    combined_text = f"Email: {email_body}\nAttachments: {' '.join(attachment_texts)}"
    prompt = SystemMessage(content=f"""Analyze the following text to classify the request type and sub-type based on these options: {json.dumps(REQUEST_TYPES)}.
    - Prioritize the email body for the primary intent, using attachments to provide supporting details.
    - Detect all applicable request types and their sub-types (if any) based on contextual understanding of the text.
    - Assign a confidence score (0.0 to 1.0) to each detected request type and sub-type, reflecting the likelihood of the classification.
    - Provide a brief reasoning for each classification based on specific phrases or context in the text.
    - Identify the primary request as the most actionable intent (e.g., a direct instruction like funding, payment, or adjustment).
    - If no sub-type is explicitly supported by the text, use null.
    Return ONLY a single JSON object with: 
      - request_types: list of dicts (type, sub_type, confidence, reasoning),
      - primary_request: dict (type, sub_type, reasoning).
    No extra text outside the JSON.""")
    human_msg = HumanMessage(content=combined_text)
    try:
        response = model.invoke([prompt, human_msg])
        print(f"DEBUG: Classify Response = '{response.content}'")
        match = re.search(r'\{[\s\S]*\}', response.content)
        if match:
            return json.loads(match.group(0))
        else:
            print(f"ERROR: No JSON in classify response: {response.content}")
            return {"error": "No valid JSON in classification response"}
    except Exception as e:
        print(f"ERROR: Classification Failed - {str(e)}")
        return {"error": f"Classification failed: {str(e)}"}

def extract_fields(request_type, email_body, attachment_texts):
    """Extract fields using Together AI"""
    fields = FIELD_MAPPING.get(request_type, [])
    model = ChatTogether(model="meta-llama/Llama-Vision-Free")
    combined_text = f"Email: {email_body}\nAttachments: {' '.join(attachment_texts)}"
    prompt = SystemMessage(content=f"""Extract the following fields from the text: {', '.join(fields)}.
    - Prioritize attachments for numerical data (e.g., amounts, account numbers) and detailed information.
    - Use the email body for contextual clues if needed.
    - For 'Sender', identify the entity or person issuing the request (e.g., from 'From:', signature, or context like 'CITIZENS BANK N.A.').
    - For 'Receiver', identify the entity or person the request is addressed to (e.g., from 'To:', 'ATTN:', or context).
    - Return ONLY a JSON object with field names as keys and extracted values as values (e.g., {{"Deal Name": "value"}}).
    - If a field is not found, use null as the value.
    No extra text outside the JSON.""")
    human_msg = HumanMessage(content=combined_text)
    try:
        response = model.invoke([prompt, human_msg])
        print(f"DEBUG: Extract Response = '{response.content}'")
        match = re.search(r'\{[\s\S]*\}', response.content)
        if match:
            return json.loads(match.group(0))
        else:
            print(f"ERROR: No JSON in extract response: {response.content}")
            return {"error": f"No valid JSON returned: {response.content}"}
    except Exception as e:
        print(f"ERROR: Field Extraction Failed - {str(e)}")
        return {"error": f"Field extraction failed: {str(e)}"}

def analyze_file(file):
    """Main analysis function for a single file (PDF or EML)"""
    attachment_texts = []
    email_body = ""

    if file.mimetype == 'application/pdf':
        images = convert_from_bytes(file.read(), dpi=200)
        for img in images:
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            text = perform_ocr(img_byte_arr)
            attachment_texts.append(text)
    elif file.mimetype == 'message/rfc822':  # MIME type for .eml
        email_body, attachment_texts = parse_eml(file)
    else:
        return {"error": "Unsupported file type. Use .pdf or .eml"}

    classification = classify_request(email_body, attachment_texts)
    if "error" in classification:
        return classification
    primary_request = classification["primary_request"]["type"]
    fields = extract_fields(primary_request, email_body, attachment_texts)
    combined_text = f"{email_body} {' '.join(attachment_texts)}"
    is_duplicate = utils.detect_duplicate(combined_text)

    return {
        "request_types": classification["request_types"],
        "primary_request": classification["primary_request"],
        "extracted_fields": fields,
        "duplicate": {
            "is_duplicate": is_duplicate,
            "reason": "High similarity to previous file" if is_duplicate else "No match found"
        }
    }