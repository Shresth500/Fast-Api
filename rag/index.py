import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
load_dotenv()


def RAG_Creation():
    client = QdrantClient(url="http://localhost:6333")

    # client.delete_collection("learning_rag")
    # client.delete_collection("rag_collection")


    pdf_path = Path(__file__).parent / "JavaNotesForProfessionals.pdf"

    loader = PyPDFLoader(file_path=str(pdf_path))

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=400
    )

    chunks = text_splitter.split_documents(docs)

    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    doc_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url="http://localhost:6333",
        collection_name="learning_rag"
    )

    print("Indexing completed!")