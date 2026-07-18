import json
import logging
from mem0 import Memory
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from agents.config import config
from agents.Domain import VALID_DOMAIN


class DecisionAgent:
    logger = logging.getLogger(__name__)
    _instance = None  # holds the single shared instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.memory_client = Memory.from_config(config)
            # These run only ONCE — on first instantiation
            cls._instance.llm = init_chat_model(
                model="llama3",
                model_provider="ollama",
                temperature=0,
                num_predict=50, # caps output — routing only needs one JSON line
            )
        return cls._instance

    def agent_output(self, user_query: str, memory_context: str):
        output_format = json.dumps({
            "domain": "one of the supported domains",
            "user_query": "user query given by the user"
        }, indent=4)

        

        domains = "\n".join(f"- {d}" for d in VALID_DOMAIN)

        prompt = f"""
            You are a routing assistant.
            Previous context: {memory_context}
            SUPPORTED DOMAINS: {domains}
            User Query: {user_query}
            OUTPUT FORMAT (respond ONLY with valid JSON, no extra text, paste the user_query as it is given by the user, and ensure the domain is one of the supported domains):
            {output_format}
        """

        self.logger.info("Fetching routing decision from LLM")
        agent = create_agent(model=self.llm, 
                             tools=[], 
                             system_prompt=prompt)
        response = agent.invoke(
            {"messages": [{"role": "user", "content": user_query}]}
        )

        print(f"Raw response from LLM: {response}")
        print(f"Raw response content: {response['messages'][-1].content_blocks}")
        print(f"user_query: {user_query}")
        last_message = response["messages"][-1]
        output_text = last_message.content   # <- this is the string you need
        content = json.loads(output_text.strip())
        domain = content.get("domain")
        if domain not in VALID_DOMAIN:
            raise ValueError(f"Unexpected domain: {domain}")

        # Don't trust content["user_query"] — use the original, guaranteed-correct value
        return {"domain": domain, "user_query": user_query}