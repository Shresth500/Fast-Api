import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from rag.meta_data_extractor import extract_meta_data, tag_chunks_with_entities
load_dotenv()

class RAGImplementation:
    @staticmethod
    def RAG_Creation(document_name:str):

        collection_name = document_name.lower().replace(" ", "_")
        client = QdrantClient(url="http://localhost:6333")

        # Skip indexing if collection already exists
        existing = [c.name for c in client.get_collections().collections]
        if collection_name in existing:
            print(f"Collection '{collection_name}' already exists. Skipping indexing.")
            return
        
        
        pdf_path = Path(__file__).parent / f"{document_name}.pdf"

        # Load once via PyPDFLoader (handles the binary PDF correctly).
        # The previous open("...").read() on a .pdf path would either raise
        # a UnicodeDecodeError or yield garbage text, since PDFs aren't plain text.
        loader = PyPDFLoader(file_path=str(pdf_path))
        docs = loader.load()
    
        # LangExtract works on a single text blob with its own internal chunking
        # (max_char_buffer / extraction_passes), so feed it the full concatenated
        # document text rather than the per-page Documents from the loader.
        full_document_text = "\n\n".join(d.page_content for d in docs)
        grounded_extractions = extract_meta_data(document_text=full_document_text)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200
        )

        chunks = tag_chunks_with_entities(text_splitter.split_documents(docs), grounded_extractions)

        embedding_model = OllamaEmbeddings(
            model="nomic-embed-text"
        )

        doc_store = QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embedding_model,
            url="http://localhost:6333",
            collection_name=document_name.lower().replace(" ", "_")
        )

        print("Indexing completed!")
