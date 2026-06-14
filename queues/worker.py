from ollama import chat
# from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
import os

from rag.index import RAG_Creation

load_dotenv()

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text"
)


def process_query(query: str):

    RAG_Creation()

    print("Searching chunks...")

    vector_db = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name="learning_rag",
        embedding=embedding_model
    )

    search_results = vector_db.similarity_search(
        query=query,
        k=5
    )

    context = "\n\n".join([
        f"Page Content: {doc.page_content}"
        for doc in search_results
    ])

    system_prompt = f"""
        You are a helpful AI Assistant.

        Answer the user's question only using the provided context.

        Context:
        {context}
        """

    response = chat(
        model="llama3",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )

    answer = response["message"]["content"]

    print(answer)
    return answer