import logging

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from mem0 import Memory
from agents.config import config


class BaseAgent:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.memory_client = Memory.from_config(config)
        self.llm_model = init_chat_model(
            model="llama3",
            model_provider="ollama",
            temperature=0.1,
            max_tokens=512,  # single kwarg for output length — don't also pass num_predict
        )

    def output(self, user_query: str, user_id: int, chat_window_id: int, vector_db,memory_context:str):
        self.logger.info("Fetching memories from mem0")
        print(f"llm object: {self.memory_client.llm}")
        print(f"llm type: {type(self.memory_client.llm)}")
        print("has generate_response:", hasattr(self.memory_client.llm, "generate_response"))

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
        agent = create_agent(
            model=self.llm_model,
            tools=[],
            system_prompt=prompt,
        )

        response = agent.invoke(
            {"messages": [{"role": "user", "content": user_query}]}
        )

        # Same extraction fix as DecisionAgent — invoke() returns a dict,
        # not an object with .content.
        output_text = response["messages"][-1].content_blocks
        print(f"Raw response from LLM: {response}")
        print(f"Raw response content: {output_text}")
        print(f"Output text: {output_text[0]['text']}")
        self.logger.info("Storing conversation in mem0")
        result = self.memory_client.add(
            messages=[
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": output_text[0]['text']},
            ],
            user_id=str(user_id),
            run_id=str(chat_window_id),
        )
        self.logger.info(f"Added: {result}")

        return output_text[0]['text']  # Return the text of the last message