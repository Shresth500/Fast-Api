from rag import RAG
from dotenv import load_dotenv
from rag_implementation import RAGImplementation

import os

load_dotenv()

class JavaRAG(RAG):
    def set_rag(self):
        java_document_name = os.getenv("JAVA_DOCUMENT")
        RAGImplementation.RAG_Creation(java_document_name)