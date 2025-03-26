# 🚀 Triage Master - GenAI Email Classification System (By Team Intelli-Triage)

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Future Enhancements](#future-enhancements)
- [Team](#team)

---

## 🎯 Introduction
Managing high volumes of customer service emails is a major challenge for financial institutions.  
Banks receive thousands of emails daily, with inquiries about **transactions, refunds, security issues, and credit card requests**.  

This project, **Triage Master - GenAI Email Classification System**, leverages **Generative AI (Llama-Vision-Free) model** to automate email triage by classifying emails into structured **Request Types** and **Sub-Types**.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
Traditional **rule-based email processing systems** often fail when emails contain unstructured or complex text.  
By using **AI-driven classification**, we can make email management more efficient and accurate, leading to:  
✅ **Faster customer support response times**  
✅ **Reduced manual effort for banking teams**  
✅ **Higher accuracy in routing emails to the correct department**  

## ⚙️ What It Does
✅ **Extracts email content** from `.eml` files  
✅ **Uses Llama-Vision-Free** to extract the content from .eml and pdf files to classify emails into **Request Type & Sub-Type**  
✅ **Not just the Request and Sub Type, provides additional details like Confidence score, Deal name, Sender, Reciever, Amount and Dates**  
✅ **Provides a user-friendly UI** to upload emails & view results  
✅ **Connects to a Flask backend** for real-time processing  

## 🛠️ How We Built It
### **1️⃣ Research & Planning**
- Studied common email classification challenges in banking.  
- Created a dataset of **real-world banking emails** for testing (both pdf and eml files).  
- Designed a taxonomy of **Request Types & Sub-Types**.  

### **2️⃣ Backend Development**
- **Built with Flask** for handling API requests.  
- **Integrated Llama-Vision-Free via ChatTogether (TogetherAI)** for AI-driven classification.  
- **Used `email` and `pdf2image` to extract email metadata & content from `.eml` and `pdf` files.  

### **3️⃣ Frontend Development**
- Created an **interactive UI** using HTML + CSS + Javascript.  
- Added **file upload functionality** for `.eml` and `.pdf` files.  
- Displayed classification results dynamically.  

### **4️⃣ Testing & Optimization**
- Fine-tuned **Llama-Vision-Free prompts** for higher classification accuracy.  
- Handled **edge cases** like empty emails, forwarded emails, and different formats.  
- Improved **API response time** by optimizing file handling.  

## 🚧 Challenges We Faced
🚀 **Challenge 1: Running Llama-Vision-Free on a Low-Memory System**  
   - Optimized model by using **quantized versions** to reduce memory footprint.  

🚀 **Challenge 2: Parsing Complex Emails**  
   - Some emails had **embedded HTML and attachments**.  
   - Used ocr and email modules and **fallback methods** to extract the correct text.  

🚀 **Challenge 3: Ensuring Accurate Classification**  
   - Fine-tuned prompts and added **post-processing filters**.  
   - Used **confidence scores** to handle uncertain classifications.  

## 🏃 How to Run
### **1️⃣ Clone the repository**
```sh
git clone https://github.com/ewfx/gaied-intelli-triage.git
cd gaied-intelli-triage
```

### **2️⃣ Backend Setup**
```sh
cd gaied-intelli-triage
cd code
cd src
cd Backend
python -m venv env (to setup virtual environment)
source env/bin/activate
pip install -r requirements.txt
python app.py
Running on http://127.0.0.1:5000
```

### **3️⃣ Frontend Setup**
```sh
cd frontend
index.html
```

Now, open **(http://127.0.0.1:5000)** to access the UI.

## 🏗️ Tech Stack
- 🔹 **Frontend:** HTML, CSS, Javascript  
- 🔹 **Backend:** Flask
- 🔹 **AI Model:** meta-llama/Llama-Vision-Free via ChatTogether  
- 🔹 **Email Processing:** `email`, `ocr` and `pdf2image`
- 🔹 **Duplicates Detection:** `TfidfVectorizer` and `Cosine similarity` (Used local db, would like to extend it by integrating with databases like MongoDB or SQL)

## 🚀 Future Enhancements
📌 **Gmail/Outlook API Integration** – Directly fetch unread emails for real-time classification.  
📌 **Multi-Language Support** – Handle emails in different languages.  
📌 **Enhanced UI Analytics** – Add a dashboard for email trends & classification stats.  
📌 **Fine-tuning LLaMA** – Improve accuracy by training on a custom dataset.  
📌 **Database Integration** – Integrating with databases like MongoDB or SQL


## 👥 Team
- **Jahangir Pasha** (Jahangir.Pasha@wellsfargo.com)
- **Murali Kuna** (Murali.Kuna@wellsfargo.com)
- **Trivedh Madala** (Trivedh.Madala@wellsfargo.com)
- **Pavankishore Kancharla** (Pavankishore.Kancharla@wellsfargo.com)
---
🚀 **This is just the beginning! Looking forward to scaling this AI-powered email triage system.**
