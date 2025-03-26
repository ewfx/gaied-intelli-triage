# 🚀 GenAI Email Classification System

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

This project, **GenAI Email Classification System**, leverages **Generative AI (LLaMA 2/3)** to automate email triage by classifying emails into structured **Request Types** and **Sub-Types**.

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
✅ **Uses LLaMA 2/3** to classify emails into **Request Type & Sub-Type**  
✅ **Provides a user-friendly UI** to upload emails & view results  
✅ **Connects to a FastAPI backend** for real-time processing  
✅ **Supports both personal and enterprise Gmail accounts**  

## 🛠️ How We Built It
### **1️⃣ Research & Planning**
- Studied common email classification challenges in banking.  
- Created a dataset of **real-world banking emails** for testing.  
- Designed a taxonomy of **Request Types & Sub-Types**.  

### **2️⃣ Backend Development**
- **Built with FastAPI** for handling API requests.  
- **Integrated LLaMA 2 via Ollama** for AI-driven classification.  
- **Used `mailparser`** to extract email metadata & content from `.eml` files.  

### **3️⃣ Frontend Development**
- Created an **interactive UI** using React + TailwindCSS.  
- Added **file upload functionality** for `.eml` files.  
- Displayed classification results dynamically.  

### **4️⃣ Testing & Optimization**
- Fine-tuned **LLaMA 2 prompts** for higher classification accuracy.  
- Handled **edge cases** like empty emails, forwarded emails, and different formats.  
- Improved **API response time** by optimizing file handling.  

## 🚧 Challenges We Faced
🚀 **Challenge 1: Running LLaMA 2 on a Low-Memory System**  
   - Optimized model by using **quantized versions** to reduce memory footprint.  

🚀 **Challenge 2: Parsing Complex Emails**  
   - Some emails had **embedded HTML and attachments**.  
   - Used `mailparser` and **fallback methods** to extract the correct text.  

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
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **3️⃣ Frontend Setup**
```sh
cd frontend
index.html
```

Now, open **http://localhost:3000** to access the UI.

## 🏗️ Tech Stack
- 🔹 **Frontend:** HTML, CSS, Javascript  
- 🔹 **Backend:** Flask, Uvicorn  
- 🔹 **AI Model:** meta-llama/Llama-Vision-Free via ChatTogether  
- 🔹 **Email Processing:** `mailparser`
- 🔹 **Duplicates Detection:** `TfidfVectorizer` and Cosine similarity

## 🚀 Future Enhancements
📌 **Gmail/Outlook API Integration** – Directly fetch unread emails for real-time classification.  
📌 **Multi-Language Support** – Handle emails in different languages.  
📌 **Enhanced UI Analytics** – Add a dashboard for email trends & classification stats.  
📌 **Fine-tuning LLaMA** – Improve accuracy by training on a custom dataset.  

## 👥 Team
- **Jahangir Pasha** (Jahangir.Pasha@wellsfargo.com)
- **Murali Kuna** (Murali.Kuna@wellsfargo.com)
- **Trivedh Madala** (Trivedh.Madala@wellsfargo.com)
- **Pavankishore Kancharla** (Pavankishore.Kancharla@wellsfargo.com)
---
🚀 **This is just the beginning! Looking forward to scaling this AI-powered email triage system.**
