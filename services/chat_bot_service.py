from mem0 import Memory
from langchain_ollama import ChatOllama

from models.ChatBot import ChatBotResponse

config = {
    "version":"v1.1",
    "embedder": {
        "provider":"ollama",
        "config":{
            "model": "nomic-embed-text"
        }
    },
    "llm":{
        "provider":"ollama",
        "config":{
            "model":"llama3"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "mem0_llama"
        }
    }
}

memory_client = Memory.from_config(config)
llm = ChatOllama(model="llama3", temperature=0.1)

def chat_app(user_query:str, user_id:int, chat_window_id:int):
    memories = memory_client.search(
                        query=user_query,
                        filters={
                            "user_id": str(user_id),
                            "run_id" : str(chat_window_id)
                        },
                        limit=5
                    )

    memory_context = "\n\n".join(memory for memory in memories)
    prompt = f"""
        You are an helpful assistant 
        Previous context: 
        {memory_context}
    """

    response = llm.invoke(prompt)

    memory_client.add(
        messages=[
            {"role":"user","content":user_query},
            {"role":"assistant","content":response.content}
        ]
    )
    return ChatBotResponse(
        status="success",
        resposne=response.content
    )