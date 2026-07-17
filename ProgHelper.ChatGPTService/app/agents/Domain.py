from agents.java_agent import JavaAgent
from agents.python_agent import PythonAgent


VALID_DOMAIN = {
    "Python Programming", 
    "Java Programming"
}

DOMAIN_AGENT = {
    "Python Programming":PythonAgent, 
    "Java Programming":JavaAgent
}