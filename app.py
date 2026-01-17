import uuid
import streamlit as st
from dotenv import load_dotenv

from processor import process_all_documents
from rag import (
    get_text_chunks,
    get_vectorstore,
    get_conversation_chain,
    clear_chroma_collection,
    generate_followup_questions,
    summarize_documents,
    process_query_with_hybrid_search,
    
)
from htmlTemplates import css, bot_template, user_template


MAX_CONVERSATION_PAIRS=5  # Keep last 5 Q&A pairs(10 items)to prevent memory bloat


def display_chat_history():
    for msg in st.session_state.messages:
        template = user_template if msg["role"] == "user" else bot_template
        st.markdown(
            template.replace("{{MSG}}", msg["content"]),
            unsafe_allow_html=True
        )


def show_sources(sources):
    if not sources:
        return

    with st.expander(" Evidence used to answer"):
        for i, doc in enumerate(sources, 1):
            st.markdown(f"**Source {i}**")
            st.markdown(
                f"<div class='source-box'>{doc.page_content[:1500]}</div>",
                unsafe_allow_html=True
            )
            if doc.metadata:
                metadata_text = " || ".join([f"**{k}**: {v}" for k, v in doc.metadata.items()])
                st.caption(metadata_text)


def main():
    load_dotenv()

    st.set_page_config(
        page_title="Smart AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown(css, unsafe_allow_html=True)

    # Session State
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4()) 
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "sources" not in st.session_state:
        st.session_state.sources = []
    if "last_answer" not in st.session_state:
        st.session_state.last_answer = ""
    if "doc_stats" not in st.session_state:
        st.session_state.doc_stats = {"total_chunks": 0, "doc_count": 0, "docs_by_type": {}}
    if "followup_questions" not in st.session_state:
        st.session_state.followup_questions = []
    if "doc_summary" not in st.session_state:
        st.session_state.doc_summary = ""
    if "raw_text" not in st.session_state:
        st.session_state.raw_text = ""
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "text_chunks" not in st.session_state:
        st.session_state.text_chunks = []
    if "sub_queries" not in st.session_state:
        st.session_state.sub_queries = None
    if "use_hybrid_search" not in st.session_state:
        st.session_state.use_hybrid_search = True
    if "use_reranking" not in st.session_state:
        st.session_state.use_reranking = True

    # Header
    st.markdown(
        """
        <div class="page-title">
            <h1> Upload Documents and Chat now </h1>
            <p> SmartBot is Advanced Retrieval-Augmented Generation System</p>
        </div>

        """,
        unsafe_allow_html=True
    )

    # Sidebar 
    with st.sidebar:
        st.markdown("<div class='sidebar-section-title'>Document Management</div>", unsafe_allow_html=True)

        if st.button("New Session", use_container_width=True, key="new_chat_btn",help="Make new session for fresh start"):
            clear_chroma_collection(st.session_state.session_id, use_gpu=True)
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages.clear()
            st.session_state.chat_history.clear()
            st.session_state.sources.clear()
            st.session_state.last_answer = ""
            st.session_state.conversation = None
            st.session_state.doc_stats = {"total_chunks": 0, "doc_count": 0, "docs_by_type": {}}
            st.session_state.followup_questions = []
            st.session_state.doc_summary = ""
            st.session_state.raw_text = ""
            st.session_state.vectorstore = None
            st.session_state.text_chunks = []
            st.session_state.sub_queries = None
            st.rerun()

        st.divider()

        with st.expander("Advanced Settings", expanded=False):
            st.session_state.use_hybrid_search = st.checkbox(
                "Hybrid Search (Semantic + BM25)",
                value=True,
                help="Combines semantic and keyword search for better accuracy if disabled it will only answer on your chats and no retrival,can disable for experiments!"
            )
            st.session_state.use_reranking = st.checkbox(
                "Cross-Encoder Reranking",
                value=True,
                help="Reorders results by relevance using cross-encoder"
            )

        st.divider()

        enable_ocr = st.toggle("Enable OCR",
                                value=True,
                                help="handles images/scanned documents"
                                )

        st.divider()

        st.markdown("**Document Statistics**")
        if st.session_state.doc_stats["doc_count"] > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Documents", st.session_state.doc_stats["doc_count"])
            with col2:
                st.metric("Text Chunks", st.session_state.doc_stats["total_chunks"])
            
            if st.session_state.doc_stats["docs_by_type"]:
                st.markdown("**Document Types:**")
                for doc_type, count in st.session_state.doc_stats["docs_by_type"].items():
                    st.caption(f"{doc_type}: {count}")
            
            st.divider()

            st.markdown("**Document Summary**")
            summary_type = st.radio(
                "Summary type:",
                ["Brief", "Detailed", "Comprehensive"],
                key="summary_type",
                horizontal=True
            )
            
            if st.button("Generate Summary", use_container_width=True, key="gen_summary"):
                with st.spinner("Generating summary..."):
                    summary = summarize_documents(
                        st.session_state.vectorstore,
                        summary_type.lower()
                    )
                    st.session_state.doc_summary = summary
            
            if st.session_state.doc_summary:
                with st.expander("View Summary", expanded=True):
                    st.markdown(st.session_state.doc_summary)

        else:
            st.caption("No documents processed yet please upload docs")


        st.divider()

        pdf_docs = st.file_uploader("PDF", type="pdf", accept_multiple_files=True)
        docx_docs = st.file_uploader("DOCX", type="docx", accept_multiple_files=True)
        pptx_docs = st.file_uploader("PPTX", type="pptx", accept_multiple_files=True)
        html_docs = st.file_uploader("HTML", type=["html", "htm"], accept_multiple_files=True)
        txt_docs = st.file_uploader("TXT / MD", type=["txt", "md"], accept_multiple_files=True)
        image_docs = st.file_uploader("Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

        if st.button("Process Documents", use_container_width=True):
            with st.spinner("Processing documents..."):
                text = process_all_documents(
                    pdf_docs, docx_docs, pptx_docs,
                    html_docs, txt_docs, image_docs,
                    enable_ocr, ""
                )

                if not text.strip():
                    st.error("No text extracted")
                    return

                chunks = get_text_chunks(text)
                vs = get_vectorstore(chunks, st.session_state.session_id, use_gpu=True)
                st.session_state.vectorstore = vs
                st.session_state.text_chunks = chunks
                st.session_state.conversation = get_conversation_chain(vs, chunks)
                


                doc_count = sum([
                    len(pdf_docs) if pdf_docs else 0,
                    len(docx_docs) if docx_docs else 0,
                    len(pptx_docs) if pptx_docs else 0,
                    len(html_docs) if html_docs else 0,
                    len(txt_docs) if txt_docs else 0,
                    len(image_docs) if image_docs else 0
                ])
                
                st.session_state.doc_stats["total_chunks"] = len(chunks)
                st.session_state.doc_stats["doc_count"] = doc_count
                st.session_state.doc_stats["docs_by_type"] = {
                    "PDF": len(pdf_docs) if pdf_docs else 0,
                    "DOCX": len(docx_docs) if docx_docs else 0,
                    "PPTX": len(pptx_docs) if pptx_docs else 0,
                    "HTML": len(html_docs) if html_docs else 0,
                    "TXT/MD": len(txt_docs) if txt_docs else 0,
                    "Images": len(image_docs) if image_docs else 0
                }
                st.session_state.doc_stats["docs_by_type"] = {
                    k: v for k, v in st.session_state.doc_stats["docs_by_type"].items() if v > 0
                }
                
                st.session_state.raw_text = text
                st.success("Documents processed successfully")
                st.rerun()

    # Chat 
    display_chat_history()

    # Main flow logic
    if prompt := st.chat_input("Ask something about your documents..."):

        if not st.session_state.conversation:
            st.warning("Please upload and process documents first")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append(prompt)

        chat_pairs = [
            (st.session_state.chat_history[i],
             st.session_state.chat_history[i + 1])
            for i in range(0, len(st.session_state.chat_history) - 1, 2)
        ]

        with st.spinner("Processing query..."):
            if st.session_state.use_hybrid_search:
                response = process_query_with_hybrid_search(
                    conversation_chain=st.session_state.conversation,
                    query=prompt,
                    chat_history=chat_pairs,
                    vectorstore=st.session_state.vectorstore,
                    text_chunks=st.session_state.text_chunks,
                    use_reranking=st.session_state.use_reranking
                )
                st.session_state.sub_queries = response.get("sub_queries")
            else:
                response = st.session_state.conversation.invoke({
                    "question": prompt,
                    "chat_history": chat_pairs
                })
                st.session_state.sub_queries = None

        answer = response["answer"]
        st.session_state.chat_history.append(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.sources = response.get("source_documents", [])
        st.session_state.last_answer = answer
        st.session_state.followup_questions = generate_followup_questions(prompt, answer)
        max_items = MAX_CONVERSATION_PAIRS * 2
        if len(st.session_state.chat_history) > max_items:
            st.session_state.chat_history = st.session_state.chat_history[-max_items:]

        st.rerun()

    # Query Decompo..
    if st.session_state.sub_queries and len(st.session_state.sub_queries) > 1:
        with st.expander("Query Analysis", expanded=False):
            st.markdown("**Sub-queries:**")
            for i, sq in enumerate(st.session_state.sub_queries, 1):
                st.markdown(f"{i}. {sq}")

    #follow up
    if st.session_state.followup_questions:
        st.divider()
        st.markdown("**Suggested Follow Up Questions:**")
        for q in st.session_state.followup_questions:
            if st.button(q, use_container_width=True, key=f"followup_{q}"):
                st.session_state.chat_history.append(q)
                st.session_state.messages.append({"role": "user", "content": q})
                
                chat_pairs = [
                    (st.session_state.chat_history[i], st.session_state.chat_history[i + 1])
                    for i in range(0, len(st.session_state.chat_history) - 1, 2)
                ]
                
                if st.session_state.use_hybrid_search:
                    response = process_query_with_hybrid_search(
                        conversation_chain=st.session_state.conversation,
                        query=q,
                        chat_history=chat_pairs,
                        vectorstore=st.session_state.vectorstore,
                        text_chunks=st.session_state.text_chunks,
                        use_reranking=st.session_state.use_reranking
                    )
                else:
                    response = st.session_state.conversation.invoke({
                        "question": q,
                        "chat_history": chat_pairs
                    })
                
                answer = response["answer"]
                st.session_state.chat_history.append(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.session_state.sources = response.get("source_documents", [])
                st.session_state.last_answer = answer
                st.session_state.followup_questions = generate_followup_questions(q, answer)
                max_items=MAX_CONVERSATION_PAIRS * 2
                if len(st.session_state.chat_history) > max_items:
                    st.session_state.chat_history = st.session_state.chat_history[-max_items:]
                
                st.rerun()

    show_sources(st.session_state.sources)


if __name__ == "__main__":
    main()