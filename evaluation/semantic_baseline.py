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
import pandas as pd

from models.ollama_client import OllamaClient
from agents.semantic_agent import SemanticRiskDetector

df = pd.read_csv(
    "data/prompt_injection_dataset.csv"
)

llm = OllamaClient()

agent = SemanticRiskDetector(llm)

predictions = []

import time

for i, (_, row) in enumerate(df.iterrows()):

    print(f"Processing {i+1}/{len(df)}")

    start = time.time()

    result = agent.analyze(row["prompt"])

    print(
        f"Completed in {time.time()-start:.2f} sec"
    )

    predictions.append(
        result["vote"]
    )