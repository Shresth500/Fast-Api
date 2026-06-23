from dotenv import load_dotenv
from BaseProgrammingAgent import BaseProgrammingAgent


load_dotenv()


class PythonAgent(BaseProgrammingAgent):
    def __init__(self):
        super().__init__("PYTHON_DOCUMENT")
    
