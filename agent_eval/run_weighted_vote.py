import os
import sys

import pandas as pd

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from trust.trust_manager import TrustManager
from coalition.weighted_vote import WeightedVote


INPUT_FILE = "results/qwen35_35b_moe/merged_results.csv"
OUTPUT_FILE = "results/qwen35_35b_moe/weighted_vote_results.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    trust_manager = TrustManager()

    weighted_voter = WeightedVote(
        trust_manager
    )

    results = []

    total = len(df)

    for _, row in df.iterrows():

        print(
            f"Processing {row['id'] + 1}/{total}"
        )

        agent_results = [

            {
                "agent": "semantic",
                "vote": row["semantic_vote"],
                "confidence": row["semantic_confidence"]
            },

            {
                "agent": "override",
                "vote": row["override_vote"],
                "confidence": row["override_confidence"]
            },

            {
                "agent": "leakage",
                "vote": row["leakage_vote"],
                "confidence": row["leakage_confidence"]
            },

            {
                "agent": "role_hijack",
                "vote": row["role_hijack_vote"],
                "confidence": row["role_hijack_confidence"]
            },

            {
                "agent": "benign_validator",
                "vote": row["benign_validator_vote"],
                "confidence": row["benign_validator_confidence"]
            }

        ]

        coalition = weighted_voter.decide(
            agent_results
        )

        prediction = coalition["verdict"]

        correct = (
            prediction == row["label"]
        )


        for agent in agent_results:

            trust_manager.update(
                agent["agent"],
                agent["vote"] == row["label"]
            )

        results.append(

            {
                "id": row["id"],
                "prompt": row["prompt"],
                "label": row["label"],

                "prediction": prediction,

                "correct": correct,

                "attack_score":
                    coalition["attack_score"],

                "benign_score":
                    coalition["benign_score"],

                "severity":
                    coalition["severity"],

                "consensus":
                    coalition["consensus"],

                "semantic_vote":
                    row["semantic_vote"],

                "override_vote":
                    row["override_vote"],

                "leakage_vote":
                    row["leakage_vote"],

                "role_hijack_vote":
                    row["role_hijack_vote"],

                "benign_validator_vote":
                    row["benign_validator_vote"],

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

    output = pd.DataFrame(
        results
    )

    output.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()

    print(
        f"Saved to {OUTPUT_FILE}"
    )

    print()

    print(
        "Accuracy:",
        output["correct"].mean()
    )


if __name__ == "__main__":
    main()