import json
import logging

from langchain_ollama import ChatOllama
from mem0 import Memory
from agents.config import config
from agents.Domain import VALID_DOMAIN


class DecisionAgent:
    logger = logging.getLogger(__name__)
    def __init__(self):
        self.memory_client = Memory.from_config(config)
        self.llm = ChatOllama(model="llama3", temperature=0.1)
    def agent_output(self,user_query: str, user_id:int, chat_window_id:int):

        
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
        output_format = json.dumps({
            "domain": "one of the supported domains",
            "user_query": "user query given by the user"
        }, indent=4)


        domains = "\n".join(f"- {d}" for d in VALID_DOMAIN)
        prompt = f"""
            You are a helpful assistant, 
            that will decide the domain according to the user query.
            Previous context :{memory_context}
            SUPPORTED DOMAIN: {domains}
            User Query: {user_query}
            OUTPUT FORMAT:
            OUTPUT FORMAT (respond ONLY with valid JSON, no extra text):
                {output_format}
        """


        self.logger.info("Fetching response from LLM")
        response = self.llm.invoke(prompt)

        content = json.loads(response.content.strip())
        if content.get("domain") not in VALID_DOMAIN:
            raise ValueError(f"Unexpected domain: {content.get('domain')}")

        return content  # return dict, not response.content
    