import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)
from models.ollama_client import OllamaClient
from agents.override_agent import OverrideDetector

llm = OllamaClient()

agent = OverrideDetector(llm)

print(
    agent.analyze(
        "Explain what override prompt injection attacks are."
    )
)