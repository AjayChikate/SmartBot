import os
from dotenv import load_dotenv

from langchain_text_splitters import CharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.chains import ConversationalRetrievalChain

from langchain.chat_models import init_chat_model




def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=300, length_function=len)
    return text_splitter.split_text(text)



def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore



def get_conversation_chain(vectorstore):
    
    if not os.getenv("GOOGLE_API_KEY"):
        
        return

    SYSTEM_PROMPT = """You are a helpful document assistant.
                    1) First, read and understand the user's question.
                    2) Re-formulate it in your mind for clarity.
                    3) Answer strictly based on the provided document context.
                    4) If you find relevant information, reply in proper format either point wise or in 2-3 paragraphs. 
                    5) If you cannot find relevant information, reply: "I did not find matching information in the provided documents."
                    Keep answers concise and factual."""

    llm = init_chat_model(
        "gemini-2.0-flash-exp",
        model_provider="google_genai",
        temperature=0.5,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    # Add persistent system instruction (safe with new LangChain versions)
    try:
        memory.chat_memory.add_message(SystemMessage(content=SYSTEM_PROMPT))
    except Exception:
        pass  # if older LangChain version doesn't support this API, ignore

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=True
    )

    return conversation_chain


