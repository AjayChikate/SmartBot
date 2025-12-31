# 🤖 SmartBot

A powerful Streamlit-based application that enables intelligent conversations with your documents using RAG (Retrieval-Augmented Generation) technology and Google's Gemini AI.

<div align="center">
<img width="300"  src="https://github.com/user-attachments/assets/cfaca4fd-2563-4558-8a3f-278a725bfee1" />
<img width="300"  src="https://github.com/user-attachments/assets/6d1a9ffd-e7b6-4dbd-8f1a-43d311801b2f" />
</div>


## ✨ Features

- 📄 **Multi-Format Support**: PDF, Word (DOCX), PowerPoint (PPTX), HTML, Text/Markdown, and Images
- 🔍 **OCR Capability**: Extract text from scanned documents and images using Tesseract
- 🧠 **Smart Retrieval**: Uses FAISS vector store with sentence transformers for accurate document retrieval
- 💬 **Conversational AI**: Powered by Google's Gemini 2.0 Flash for intelligent responses
- 📚 **Source References**: View exact document snippets used to generate answers
- 🎨 **Modern UI**: Clean, intuitive interface with custom styling
- 💾 **Session Memory**: Maintains conversation context throughout your session

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AjayChikate/SmartBot.git
cd smartbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_api_key_here
TESSERACT_CMD=C:/Program Files/Tesseract-OCR/tesseract.exe
POPPLER_PATH=C:/Program Files/poppler/Library/bin
```

4. **Run the application**
```bash
streamlit run app.py
```

## 📦 Dependencies
```txt
streamlit
python-dotenv
langchain
langchain-community
langchain-google-genai
faiss-cpu
sentence-transformers
pdfplumber
PyPDF2
pdf2image
python-docx
python-pptx
beautifulsoup4
Pillow
pytesseract
```

## 🎯 Usage

1. **Upload Documents**: Use the sidebar to upload one or more documents in supported formats
2. **Enable OCR**: Toggle OCR if you have scanned documents or images with text
3. **Process**: Click "🚀 Process Documents" to build the knowledge base
4. **Chat**: Ask questions about your documents in natural language
5. **View Sources**: Expand the source references to see which document sections were used

## 🏗️ Project Structure
```
SmartBot/
│
├── app.py                 # Main Streamlit application
├── rag.py                 # RAG pipeline (chunking, vectorstore, conversation chain)
├── processor.py           # Document processing orchestrator
├── extraction.py          # Text extraction for various file formats
├── ocr.py                 # OCR functionality using Tesseract
├── htmlTemplates.py       # CSS and HTML templates for UI
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (not in repo)
└── README.md            
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

⭐ If you find this project helpful, please consider giving it a star!
