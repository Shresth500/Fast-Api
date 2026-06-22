
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore


embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)



def load_vector_store(collection_name:str):
    """Connect to existing Qdrant Cloud collection (skip re-indexing)."""
    vector_db = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name=collection_name.lower().replace(" ", "_"),
        embedding=embedding_model
    )
    return vector_db