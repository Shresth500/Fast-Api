from orchestrator_agent import OrchestratorAgent


if __name__ == '__main__':
    workflow = OrchestratorAgent()
    user_id, chat_window_id=1,1

    while True:
        user_query = input("Enter your query: ")
        if user_query.lower() == "exit":
            break
        workflow.agent_output(
            user_query=user_query,
            user_id=user_id,
            chat_window_id=chat_window_id
        )