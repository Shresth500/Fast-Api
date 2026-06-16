import logging

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
logger = logging.getLogger(__name__)

def chat_app(user_query:str, user_id:int, chat_window_id:int):
    logger.info(f"Getting the contents from the mem0")
    memories = memory_client.search(
                        query=user_query,
                        filters={
                            "user_id": str(user_id),
                            "run_id" : str(chat_window_id)
                        },
                        limit=5
                    )
    logger.info(f"Previous Messages close to the User-query:{memories}")
    memory_context = "\n\n".join(memory["memory"] for memory in memories.get("results", []))
    prompt = f"""
        You are a helpful assistant 
        Previous context: 
        {memory_context}
        User: {user_query}
    """
    logger.info(f"Loading the response from the LLM")
    response = llm.invoke(prompt)

    logger.info(f"Got the Response from the LLM")
    logger.info(f"Loading the conversation inside the mem0")
    memory_client.add(
        messages=[
            {"role":"user","content":user_query},
            {"role":"assistant","content":response.content}
        ],
        user_id=str(user_id),
        run_id=str(chat_window_id)
    )
    return ChatBotResponse(
        status="success",
        resposne=response.content
    )