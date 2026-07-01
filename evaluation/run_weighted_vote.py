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

from models.api_client import APIClient

from agents.semantic_agent import SemanticRiskDetector
from agents.override_agent import OverrideDetector
from agents.leakage_agent import LeakageDetector
from agents.role_hijack_agent import RoleHijackDetector
from agents.benign_validator import BenignIntentValidator
from judge.llm_judge import LLMJudge
from trust.trust_manager import TrustManager
from coalition.weighted_vote import WeightedVote


df = pd.read_csv(
    "data/prompt_injection_dataset.csv"
)

llm = APIClient()

semantic = SemanticRiskDetector(llm)
override = OverrideDetector(llm)
leakage = LeakageDetector(llm)
role_hijack = RoleHijackDetector(llm)
benign_validator = BenignIntentValidator(llm)

trust_manager = TrustManager()

weighted_voter = WeightedVote(
    trust_manager
)
judge = LLMJudge(
    llm
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
    print(coalition_result)
    judge_result = judge.evaluate(
    prompt,
    coalition_result,
    agent_results
    )

    prediction = coalition_result[
        "verdict"
    ]

    correct = (
        prediction == label
    )
    for agent_result in agent_results:

        agent_name = agent_result["agent"]

        agent_correct = (
            agent_result["vote"]
            == label
        )

        trust_manager.update(
            agent_name,
            agent_correct
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
            ],
        "severity":
            coalition_result[
                "severity"
            ],

        "consensus":
            coalition_result[
                "consensus"
            ],

        "judge_explanation":
            judge_result[
                "explanation"
            ],

        "semantic_vote":
            agent_results[0]["vote"],

        "override_vote":
            agent_results[1]["vote"],

        "leakage_vote":
            agent_results[2]["vote"],

        "role_hijack_vote":
            agent_results[3]["vote"],

        "benign_validator_vote":
            agent_results[4]["vote"],

        "semantic_trust":
            trust_manager.get_trust(
                "semantic"
            ),

        "override_trust":
            trust_manager.get_trust(
                "override"
            ),

        "leakage_trust":
            trust_manager.get_trust(
                "leakage"
            ),

        "role_hijack_trust":
            trust_manager.get_trust(
                "role_hijack"
            ),

        "benign_validator_trust":
            trust_manager.get_trust(
                "benign_validator"
            )
    }
)

results_df = pd.DataFrame(
    results
)

results_df.to_csv(
    "results/qwen3_4b/results.csv",
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