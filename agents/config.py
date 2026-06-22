config = {
    "version":"v1.1",
    "embedder": {
        "provider":"ollama",
        "config":{
            "model": "nomic-embed-text"
        }
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:latest",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434",  # Ensure this URL is correct
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "mem0_llama",
            "embedding_model_dims": 768, 
        }
    }
}

