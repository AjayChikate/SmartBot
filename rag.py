import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings, SentenceTransformerEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from typing import List
import re

# System prompt
SYSTEM_PROMPT = """You are a helpful AI assistant that answers questions based on the provided documents. 
Your role is to:
1. Provide accurate and concise answers based on document content
2. Cite which parts of the documents you're referencing
3. Ask clarifying questions if needed
4. Maintain a conversational and friendly tone
5. Be honest when you don't have information in the documents"""

# Custom prompt template
# _DEFAULT_TEMPLATE = """{context}

# {chat_history}
# Human: {question}
# Assistant:"""

# CUSTOM_PROMPT = PromptTemplate(
#     input_variables=["context", "chat_history", "question"],
#     template=_DEFAULT_TEMPLATE,
# )


def get_text_chunks(text: str):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=400,
        chunk_overlap=80
    )
    return splitter.split_text(text)


def get_vectorstore(text_chunks, session_id, use_gpu: bool = True):
    
    import torch
    
    # Check if GPU is actually available
    has_gpu = torch.cuda.is_available()
    device = "cuda" if (use_gpu and has_gpu) else "cpu"
    
    if use_gpu and not has_gpu:
        print("GPU was not available. Using CPU instead.")
    
    embeddings = SentenceTransformerEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={"device": device}
    )
    
    print(f"Embeddings using: {device.upper()}")

    return Chroma.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        collection_name=f"session_{session_id}",
        persist_directory="./chroma_db"
    )


#  Query decompo.. - breaks complex queries into sub-queries

def decompose_query(question: str) -> List[str]:
    
    # if query is complexx (long + has multiple parts)
    has_multiple_parts = any(word in question.lower() for word in ['and', 'also', 'additionally', 'furthermore', 'moreover'])
    is_long = len(question) > 50
    
    if not (is_long and has_multiple_parts):
        return [question]  # original
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0.2
    )
    
    prompt = f"""Break this complex question into 2-5 simpler sub-questions that can be answered independently.
                Each sub-question should target a specific aspect of the original question.

                Original Question: {question}

                Output format (one per line):
                1. [sub-question 1]
                2. [sub-question 2]
                ...

                Sub-questions:"""
    
    try:
        response = llm.invoke(prompt)
        sub_queries = response.content.strip().split('\n')
        sub_queries = [q.strip() for q in sub_queries if q.strip() and q[0].isdigit()]
        sub_queries = [re.sub(r'^\d+\.\s*', '', q) for q in sub_queries] #extra cleaning
        
        if len(sub_queries) >= 2:
            print(f"Query decomposed into {len(sub_queries)} sub-queries")
            return sub_queries
        else:
            return [question]
            
    except Exception as e:
        print(f"Query decomposition error: {e}")
        return [question]


#    Hybrid Semantic+BM25+Reranking

def create_hybrid_retriever(vectorstore, text_chunks, k: int = 8):
    #k: no of docs to retrieve

    semantic_retriever = vectorstore.as_retriever(
        search_kwargs={"k": k}
    )
    
    bm25_retriever = BM25Retriever.from_texts(text_chunks)
    bm25_retriever.k = k
    
    # Ensemble
    hybrid_retriever = EnsembleRetriever(
        retrievers=[semantic_retriever, bm25_retriever],
        weights=[0.6, 0.4]
    )
    
    print("Hybrid retriever created!!")
    return hybrid_retriever


# rerankings

def rerank_documents(docs, query: str, top_k: int = 5):
  
    try:
        from sentence_transformers import CrossEncoder
        
        reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')# Lightweight cross-encoder for reranking
        doc_texts = [doc.page_content for doc in docs]
        pairs = [[query, doc_text] for doc_text in doc_texts]
        scores = reranker.predict(pairs)
        
        # Sort
        scored_docs = list(zip(docs, scores))
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        reranked = [doc for doc, score in scored_docs[:top_k]]
        print(f"Reranked {len(docs)} docs → top {top_k}")
        return reranked
        
    except ImportError:
        print("sentence-transformers not installed. Skipping reranking.")
        print(" Install: pip install sentence-transformers")
        return docs[:top_k]
    except Exception as e:
        print(f"Reranking error: {e}")
        return docs[:top_k]


def get_conversation_chain(vectorstore, text_chunks):
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0.3,
        system_prompt=SYSTEM_PROMPT
    )

    hybrid_retriever = create_hybrid_retriever(vectorstore, text_chunks, k=8)

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=hybrid_retriever,
        return_source_documents=True,
        verbose=False
    )


# for complex queries like those broke into subqueries..

def process_query_with_hybrid_search(conversation_chain, query: str, chat_history, 
                                     vectorstore, text_chunks, use_reranking: bool = True):
   
    sub_queries = decompose_query(query)
    
    if len(sub_queries) > 1:
        # Multiqueries
        print(f"Processing {len(sub_queries)} sub-queries...")
        
        all_docs = []
        hybrid_retriever = create_hybrid_retriever(vectorstore, text_chunks, k=5)
        
        for i, sq in enumerate(sub_queries, 1):
            print(f"  {i}. {sq}")
            docs = hybrid_retriever.get_relevant_documents(sq)
            all_docs.extend(docs)
        
        seen = set()# Remove duplicates
        unique_docs = []
        for doc in all_docs:
            if doc.page_content not in seen:
                unique_docs.append(doc)
                seen.add(doc.page_content)
        
        if use_reranking and len(unique_docs) > 5:
            final_docs = rerank_documents(unique_docs, query, top_k=5)
        else:
            final_docs = unique_docs[:5]
        
        context = "\n\n".join([doc.page_content for doc in final_docs])
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=0.3
        )
        
        answer_prompt = f"""Based on the following context, answer this question comprehensively:

                                Question: {query}

                                Context:
                                {context}

                                Provide a detailed answer:"""
        
        response = llm.invoke(answer_prompt)
        
        return {
            "answer": response.content,
            "source_documents": final_docs,
            "sub_queries": sub_queries
        }
    



    else:
        # Simple query
        hybrid_retriever = create_hybrid_retriever(vectorstore, text_chunks, k=8)
        docs = hybrid_retriever.get_relevant_documents(query)
        
        if use_reranking:
            docs = rerank_documents(docs, query, top_k=5)
        
        result = conversation_chain({"question": query, "chat_history": chat_history})
        result["sub_queries"] = None
        return result


def clear_chroma_collection(session_id, use_gpu: bool = True):
   
    import torch
    
    try:
        has_gpu = torch.cuda.is_available()
        device = "cuda" if (has_gpu) else "cpu"
        print(device)
        embeddings = SentenceTransformerEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={"device": device}
        )
        vs = Chroma(
            collection_name=f"session_{session_id}",
            embedding_function=embeddings,
            persist_directory="./chroma_db"
        )
        vs.delete_collection()
        return True
    except Exception as e:
        print("Chroma cleanup error:", e)
        return False


def generate_followup_questions(question: str, answer: str) -> list:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0.5
    )
    
    prompt = f"""Based on this Q&A, generate 3 concise follow-up questions that would deepen understanding.
                Each question should be 1 line, practical, and relevant.

                Original Question: {question}
                Answer: {answer}

                Generate 3 follow-up questions (one per line, numbered):"""
    
    try:
        response = llm.invoke(prompt)
        questions = response.content.strip().split('\n')
        questions = [q.strip() for q in questions if q.strip() and q[0].isdigit()]
        questions = [q.split('. ', 1)[-1] if '. ' in q else q for q in questions]
        return questions[:3]
    except Exception as e:
        print(f"Error generating follow-up questions: {e}")
        return []


def summarize_documents(vectorstore, summary_type: str = "brief") -> str:
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0.3
    )

    semantic_queries = [   # Multiquery semantic search captures different document aspects
        "main topics and key concepts",
        "important findings and results",
        "technical details and specifications",
        "examples and case studies",
        "conclusions and recommendations",
        "problem statements and solutions",
        "background and context",
        "data and statistics"
    ]
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    all_chunks = []
    seen_content = set()
    
    for query in semantic_queries:
        try:
            docs = retriever.invoke(query)
            for doc in docs:
                content = doc.page_content.strip()
                if content and content not in seen_content:
                    all_chunks.append(content)
                    seen_content.add(content)
        except Exception as e:
            print(f"Query '{query}' error: {e}")
            pass
    
    context = "\n\n".join(all_chunks[:20])
    
    length_guide = {
        "brief": "2-3 paragraphs with key points",
        "detailed": "5-7 paragraphs with main topics and important details",
        "comprehensive": "Complete summary covering all major topics and subtopics"
    }
    
    prompt = f"""Create a {length_guide.get(summary_type, 'brief')} summary.
            Organize by topic, maintain logical flow, highlight key information.

            Document Content:
            {context}

            Provide the summary:"""
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error summarizing: {e}")
        return "Error generating summary. Please try again."
    

