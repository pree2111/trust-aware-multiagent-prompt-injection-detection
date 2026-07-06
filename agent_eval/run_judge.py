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

from models.api_client import APIClient
from judge.llm_judge import LLMJudge


WEIGHTED_FILE = "results/qwen35_122b_moe/weighted_vote_results.csv"
MERGED_FILE = "results/qwen35_122b_moe/merged_results.csv"
OUTPUT_FILE = "results/qwen35_122b_moe/final_results.csv"


def main():

    weighted = pd.read_csv(
        WEIGHTED_FILE
    )

    merged = pd.read_csv(
        MERGED_FILE
    )[
        [
            "id",
            "semantic_confidence",
            "override_confidence",
            "leakage_confidence",
            "role_hijack_confidence",
            "benign_validator_confidence",
        ]
    ]

    df = weighted.merge(
        merged,
        on="id",
        how="left"
    )

    llm = APIClient()

    judge = LLMJudge(
        llm
    )

    total = len(df)


    if os.path.exists(OUTPUT_FILE):

        existing = pd.read_csv(
            OUTPUT_FILE
        )

        explanations = existing[
            "judge_explanation"
        ].tolist()

        start = len(existing)

        print(
            f"Resuming from row {start + 1}"
        )

    else:

        explanations = []

        start = 0

    

    for _, row in df.iloc[start:].iterrows():

        print(
            f"Judging {row['id'] + 1}/{total}"
        )

        coalition_result = {

            "verdict":
                row["prediction"],

            "attack_score":
                row["attack_score"],

            "benign_score":
                row["benign_score"],

            "severity":
                row["severity"],

            "consensus":
                row["consensus"]

        }

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

        try:

            result = judge.evaluate(
                prompt=row["prompt"],
                coalition_result=coalition_result,
                agent_results=agent_results,
                row_id=int(row["id"])
            )

            explanations.append(
                result["explanation"]
            )

        except Exception as e:

            print(
                f"ERROR on row {row['id'] + 1}: {e}"
            )

            explanations.append(
                "Judge Error"
            )


        current = df.iloc[
            :len(explanations)
        ].copy()

        current["judge_explanation"] = explanations

        current.to_csv(
            OUTPUT_FILE,
            index=False
        )

    print()

    print(
        f"Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()