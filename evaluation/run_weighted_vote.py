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
from agents.override_agent import OverrideDetector
from agents.leakage_agent import LeakageDetector
from agents.role_hijack_agent import RoleHijackDetector
from agents.benign_validator import BenignIntentValidator

from trust.trust_manager import TrustManager
from coalition.weighted_vote import WeightedVote


df = pd.read_csv(
    "data/prompt_injection_dataset.csv"
)

llm = OllamaClient()

semantic = SemanticRiskDetector(llm)
override = OverrideDetector(llm)
leakage = LeakageDetector(llm)
role_hijack = RoleHijackDetector(llm)
benign_validator = BenignIntentValidator(llm)

trust_manager = TrustManager()

weighted_voter = WeightedVote(
    trust_manager
)

results = []

for i, (_, row) in enumerate(df.iterrows()):

    print(
        f"Processing {i+1}/{len(df)}"
    )

    prompt = row["prompt"]

    label = row["label"]

    agent_results = []

    # Semantic
    result = semantic.analyze(prompt)

    result["agent"] = "semantic"

    agent_results.append(result)

    # Override
    result = override.analyze(prompt)

    result["agent"] = "override"

    agent_results.append(result)

    # Leakage
    result = leakage.analyze(prompt)

    result["agent"] = "leakage"

    agent_results.append(result)
 
    # Role Hijack
    result = role_hijack.analyze(prompt)

    result["agent"] = "role_hijack"

    agent_results.append(result)

    # Benign Validator
    result = benign_validator.analyze(prompt)

    result["agent"] = "benign_validator"

    agent_results.append(result)

    coalition_result = weighted_voter.decide(
        agent_results
    )

    prediction = coalition_result[
        "verdict"
    ]

    correct = (
        prediction == label
    )

    results.append(
        {
            "prompt": prompt,
            "label": label,
            "prediction": prediction,
            "correct": correct,
            "attack_score":
                coalition_result[
                    "attack_score"
                ],
            "benign_score":
                coalition_result[
                    "benign_score"
                ]
        }
    )

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    "results/results.csv",
    index=False
)

print()

print(
    results_df["correct"]
    .mean()
)

print(
    "Finished."
)