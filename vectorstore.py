from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import os

def create_vectorstore(docs, persist_directory="./chroma_db"):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=100,
        add_start_index=True,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    all_splits = text_splitter.split_documents(docs)
    
    if all_splits:
        local_embeddings = OllamaEmbeddings(model="all-minilm")
        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=local_embeddings,
            persist_directory=persist_directory
        )
        vectorstore.persist()
        return vectorstore
    else:
        print("No content to create vectorstore")
        return None