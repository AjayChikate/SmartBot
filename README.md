# 🤖 SmartBot

A powerful Streamlit-based application that enables intelligent conversations with your documents using Advanced RAG (Retrieval-Augmented Generation) technology and Google's Gemini AI.

<div align="center">
<img width="400"  alt="Screenshot 2026-01-17 213846" src="https://github.com/user-attachments/assets/1e06bbd3-cf1d-4f1e-bf22-ce9dacad9dfc" />
<img width="400"  alt="Screenshot 2026-01-17 214051" src="https://github.com/user-attachments/assets/73dc94d0-d52c-4260-a76b-3514d53ec746" />
<img width="400"  alt="Screenshot 2026-01-17 214153" src="https://github.com/user-attachments/assets/b38bdc3f-9d6f-48f4-adc4-060f727178b6" />
<img width="400"  alt="Screenshot 2026-01-17 214508" src="https://github.com/user-attachments/assets/224b4c79-1128-4545-9662-8432245af040" />
<img width="400"  alt="Screenshot 2026-01-17 214631" src="https://github.com/user-attachments/assets/0b016bda-ab1a-43c7-aa2b-fa7de8df494d" />


</div>


## ✨ Features

- 📄 **Multi-Format Support**: PDF, Word (DOCX), PowerPoint (PPTX), HTML, Text/Markdown, and Images
- 🧠 **Smart Retrieval**: Uses FAISS vector store with sentence transformers for accurate document retrieval
- 💬 **Conversational AI**: Powered by Google's Gemini Flash for intelligent responses
- 📚 **Source References**: View exact document snippets used to generate answers
- 🎨 **Modern UI**: Clean, intuitive interface with custom styling
- 💾 **Session Memory**: Maintains conversation context throughout your session


## 🧠 Advanced Features 

- 🔍 **OCR Capability**: Extract text from scanned documents and images using Tesseract
- 🔄 **Hybrid Search**: Combines semantic search (embeddings) with BM25 keyword matching
- 🎯 **Query Decomposition**: Breaks complex queries into sub-questions for better accuracy
- 📊 **Document Reranking**: Uses cross-encoder models to rank retrieved documents by relevance
- 📝 **Smart Summaries**: Generate brief, detailed, or comprehensive document summaries
- ❓ **Follow-up Questions**: Auto-generates contextual follow-up questions

  
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



## 🎯 Usage

1. **Upload Documents**: Use the sidebar to upload one or more documents in supported formats
2. **Enable OCR**: Toggle OCR if you have scanned documents or images with text
3. **Process**: Click "Process Documents" to build the knowledge base
4. **Chat**: Ask questions about your documents in natural language
5. **View Sources**: Expand the source references to see which document sections were used
6. **Follow ups**: Click follow-up questions to dive deeper
7. **Summary**: Generate document summaries (Brief/Detailed/Comprehensive)

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


## 📊 Metrics

- **Embedding Model**: BAAI/bge-small-en-v1.5 (384 dimensions)
- **Reranking Model**: cross-encoder/ms-marco-MiniLM-L-6-v2
- **Vector Store**: Chroma (SQLite-backed)
- **LLM**: Google Gemini Flash
  

## 🚀 Performance Tips

1. **GPU Acceleration**: Enable for faster embeddings
   - Requires CUDA-capable NVIDIA GPU
   - ~3-5x faster embedding generation

2. **Chunking Strategy**: 
   - Smaller chunks (200-300): Better precision
   - Larger chunks (500-600): Better context

3. **Retrieval Count**:
   - Small documents: k=4-5
   - Large documents: k=8-10

4. **Reranking**: Disable for <5 retrieved docs
   
  
## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

⭐ If you find this project helpful, please consider giving it a star!
