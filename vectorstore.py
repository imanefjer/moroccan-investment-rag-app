from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def create_vectorstore(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        add_start_index=True,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    all_splits = text_splitter.split_documents(docs)
    
    if all_splits:
        local_embeddings = OllamaEmbeddings(model="all-minilm")
        vectorstore = Chroma.from_documents(documents=all_splits, embedding=local_embeddings)
        return vectorstore
    else:
        print("No content to create vectorstore")
        return None