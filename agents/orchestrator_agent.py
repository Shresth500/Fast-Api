import logging

from agent import Agent
from Domain import *
from decision_agent import DecisionAgent


class OrchestratorAgent(Agent):
    logger = logging.getLogger(__name__)
    def agent_output(self, user_query: str, user_id: int, chat_window_id: int):
        try:
            decision_agent=DecisionAgent.agent_output(user_query)
            domain = decision_agent.get("domain")
            programming_agent = DOMAIN_AGENT[domain]()
            print(programming_agent.agent_output(user_query, user_id, chat_window_id))
                    
        except Exception as e:
            self.logger.error(f"Error: {e}")
            return "Sorry, something went wrong. Please try again."

