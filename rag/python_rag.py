from rag import RAG
from dotenv import load_dotenv
from rag_implementation import RAGImplementation

import os


load_dotenv()

class PythonRAG(RAG):
    def set_rag(self):
        python_document_name = os.getenv("PYTHON_DOCUMENT")
        RAGImplementation.RAG_Creation(python_document_name)