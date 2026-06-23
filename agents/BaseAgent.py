import logging

from langchain_ollama import ChatOllama
from mem0 import Memory
from agents.config import config



class BaseAgent:
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.memory_client = Memory.from_config(config)
        self.llm = ChatOllama(model="llama3", temperature=0.1)
    def output(self,user_query:str,user_id:int,
               chat_window_id:int,vector_db):
        self.logger.info("Fetching memories from mem0")
        memories = self.memory_client.search(
            query=user_query,
            filters={
                "user_id": str(user_id),
                "run_id": str(chat_window_id)
            },
            limit=5
        )
        self.logger.info(f"Previous content: {memories}")
        print(memories)
        memory_context = "\n\n".join(
            memory["memory"] for memory in memories.get("results", [])
        )

        search_results = vector_db.similarity_search(query=user_query)
        context = "\n\n".join(
            f"Page Content: {doc.page_content}" for doc in search_results
        )

        # Guard empty memory context
        memory_section = f"Previous context:\n{memory_context}\n" if memory_context else ""

        prompt = f"""
            You are an helpful programming assistant.

            {memory_section}
            User: {user_query}

            Answer the user's question only using the provided context.

            Context:
            {context}
        """

        self.logger.info("Fetching response from LLM")
        response = self.llm.invoke(prompt)

        self.logger.info("Storing conversation in mem0")
        result = self.memory_client.add(
            messages=[
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": response.content}
            ],
            user_id=str(user_id),
            run_id=str(chat_window_id)
        )
        self.logger.info(f"Added: {result}")
        print(result)
        return response.content 