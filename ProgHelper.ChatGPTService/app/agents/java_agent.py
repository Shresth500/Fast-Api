from dotenv import load_dotenv
from agents.BaseProgrammingAgent import BaseProgrammingAgent


load_dotenv()
class JavaAgent(BaseProgrammingAgent):
    def __init__(self):
        super().__init__("JAVA_DOCUMENT")