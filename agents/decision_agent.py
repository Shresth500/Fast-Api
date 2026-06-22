import json
import logging

from langchain_ollama import ChatOllama

from agent import Agent
from Domain import VALID_DOMAIN


class DecisionAgent:
    @staticmethod
    def agent_output( user_query: str):
        logger = logging.getLogger(__name__)
        llm = ChatOllama(model="llama3", temperature=0.1)
        output_format = json.dumps({
            "domain": "one of the supported domains",
            "user_query": "user query given by the user"
        }, indent=4)


        domains = "\n".join(f"- {d}" for d in VALID_DOMAIN)
        prompt = f"""
            You are a helpful assistant, 
            that will decide the domain according to the user query.
            SUPPORTED DOMAIN: {domains}
            User Query: {user_query}
            OUTPUT FORMAT:
            OUTPUT FORMAT (respond ONLY with valid JSON, no extra text):
                {output_format}
        """


        logger.info("Fetching response from LLM")
        response = llm.invoke(prompt)

        content = json.loads(response.content.strip())
        if content.get("domain") not in VALID_DOMAIN:
            raise ValueError(f"Unexpected domain: {content.get('domain')}")

        return content  # return dict, not response.content
    