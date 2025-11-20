import os
import streamlit as st
from dotenv import load_dotenv
from processor import process_all_documents
from rag import get_text_chunks, get_conversation_chain, get_vectorstore
from htmlTemplates import css, bot_template, user_template


import warnings
warnings.filterwarnings("ignore", message="Convert_system_message_to_human will be deprecated!")



def display_chat_history():
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(user_template.replace("{{MSG}}", msg["content"]), unsafe_allow_html=True)
            else:
                st.markdown(bot_template.replace("{{MSG}}", msg["content"]), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">💬</div>
            <div class="empty-state-text">Upload your documents and start chatting</div>
            <div class="empty-state-subtext">Supports PDF, Word, PowerPoint, HTML, Text & Images</div>
        </div>
        """, unsafe_allow_html=True)







def main():
    load_dotenv()
    st.set_page_config(
        page_title="AI Document Assistant", 
        page_icon="🤖", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("⚠️ Please set GOOGLE_API_KEY in your .env file!")
        st.info("Get your API key from: https://makersuite.google.com/app/apikey")
        return
    
    
    
    
    
    st.markdown(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sources" not in st.session_state:
        st.session_state.sources = []
    
    st.markdown("""
    <div class="main-header">
        <div class="header-icon">🤖</div>
        <h1>AI Document Assistant</h1>
        <p>Intelligent document analysis powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown('<div class="sidebar-header">⚙️ Settings</div>', unsafe_allow_html=True)
        enable_ocr = st.toggle("🔍 Enable OCR", value=True, help="Extract text from scanned documents and images in PDFs")
        
        st.markdown("---")
        st.markdown('<div class="sidebar-header">📁 Upload Documents</div>', unsafe_allow_html=True)
        
        pdf_docs = st.file_uploader("📄 PDF Files", accept_multiple_files=True, type=['pdf'])
        docx_docs = st.file_uploader("📝 Word Documents", accept_multiple_files=True, type=['docx'])
        pptx_docs = st.file_uploader("📊 PowerPoint Files", accept_multiple_files=True, type=['pptx'])
        html_docs = st.file_uploader("🌐 HTML Files", accept_multiple_files=True, type=['html', 'htm'])
        txt_docs = st.file_uploader("📃 Text/Markdown", accept_multiple_files=True, type=['txt', 'md'])
        image_docs = st.file_uploader("🖼️ Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'tiff'])
        
        total_files = len(pdf_docs or []) + len(docx_docs or []) + len(pptx_docs or []) + len(html_docs or []) + len(txt_docs or []) + len(image_docs or [])
        
        if total_files > 0:
            st.markdown(f'<div class="file-counter">✅ {total_files} file(s) uploaded</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🚀 Process Documents", type="primary", use_container_width=True):
            if total_files == 0:
                st.error("❌ Please upload at least one document!")
            else:
                with st.spinner("🔄 Processing your documents..."):
                    progress_bar = st.progress(0)
                    status = st.empty()
                    
                    status.info("📄 Reading documents...")
                    progress_bar.progress(20)
                    poppler_path = ""
                    all_text = process_all_documents(pdf_docs, docx_docs, pptx_docs, html_docs, txt_docs, image_docs, enable_ocr, poppler_path)
                    
                    if not all_text.strip():
                        st.error("❌ No text could be extracted from the documents!")
                    else:
                        status.info("✂️ Creating text chunks...")
                        progress_bar.progress(50)
                        text_chunks = get_text_chunks(all_text)
                        
                        status.info("🧠 Building knowledge base...")
                        progress_bar.progress(75)
                        vectorstore = get_vectorstore(text_chunks)
                        
                        status.info("🔗 Setting up AI assistant...")
                        progress_bar.progress(90)
                        st.session_state.conversation = get_conversation_chain(vectorstore)
                        
                        progress_bar.progress(100)
                        status.success(f"✅ Successfully processed {len(text_chunks)} text chunks!")
                        st.balloons()
        
        st.markdown("---")
        st.markdown('<div class="sidebar-footer">Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)
    
    display_chat_history()
    
    if prompt := st.chat_input("💬 Ask me anything about your documents..."):
        if st.session_state.conversation is None:
            st.warning("⚠️ Please upload and process documents first!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.spinner("🤔 Analyzing..."):
                try:
                    response = st.session_state.conversation.invoke({"question": prompt})
                    answer = response.get('answer', '')
                    st.session_state.sources = response.get('source_documents', [])
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            st.rerun()
    
    if st.session_state.sources and len(st.session_state.messages) > 0:
        with st.expander("📚 View Source References", expanded=False):
            for idx, doc in enumerate(st.session_state.sources, 1):
                st.markdown(f"**📄 Source {idx}**")
                snippet = doc.page_content[:400] + "..." if len(doc.page_content) > 400 else doc.page_content
                st.markdown(f'<div class="source-box">{snippet}</div>', unsafe_allow_html=True)
                if idx < len(st.session_state.sources):
                    st.markdown("---")

if __name__ == '__main__':
    main()