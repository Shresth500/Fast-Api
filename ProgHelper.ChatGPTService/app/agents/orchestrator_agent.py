import logging
from mem0 import Memory
from agents.config import config
from agents.agent import Agent
from agents.Domain import *
from rag.python_rag import PythonRAG
from rag.java_rag import JavaRAG
from agents.decision_agent import DecisionAgent


class LoadRAG:
    @staticmethod
    def load_rag():
        rag_collection=[
            PythonRAG(),
            # JavaRAG()
        ]
        for rag in rag_collection:
            rag.set_rag()

class OrchestratorAgent(Agent):
    logger = logging.getLogger(__name__)
    def __init__(self):
        super().__init__()
        self.memory_client = Memory.from_config(config)
        LoadRAG.load_rag()
    def agent_output(self, user_query: str, user_id: int, chat_window_id: int):
        try:
            memories = self.memory_client.search(
                query=user_query,
                filters={
                    "user_id": str(user_id),
                    "run_id": str(chat_window_id)
                },
                limit=5
            )
            self.logger.info(f"Previous content: {memories}")
            memory_context = "\n\n".join(
                memory["memory"] for memory in memories.get("results", [])
            )
            decision_agent=DecisionAgent()
            response = decision_agent.agent_output(user_query=user_query,memory_context=memory_context)
            print(f"Routing decision: {response}")
            domain = response.get("domain")
            programming_agent = DOMAIN_AGENT[domain]()
            response=programming_agent.agent_output(user_query, user_id, chat_window_id,memory_context)
            print(f"Response from {domain} agent: {response}")
            return response
                    
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return "Sorry, something went wrong. Please try again."

