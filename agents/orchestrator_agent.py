import logging

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
            JavaRAG()
        ]
        for rag in rag_collection:
            rag.set_rag()

class OrchestratorAgent(Agent):
    logger = logging.getLogger(__name__)
    def __init__(self):
        super().__init__()
        LoadRAG.load_rag()
    def agent_output(self, user_query: str, user_id: int, chat_window_id: int):
        try:
            decision_agent=DecisionAgent()
            response = decision_agent.agent_output(user_query=user_query, user_id=user_id, chat_window_id=chat_window_id)
            domain = response.get("domain")
            programming_agent = DOMAIN_AGENT[domain]()
            response=programming_agent.agent_output(user_query, user_id, chat_window_id)
            return response
                    
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return "Sorry, something went wrong. Please try again."

