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


FINAL_FILE = "results/qwen35_122b_moe/final_results.csv"


def main():

    if not os.path.exists(FINAL_FILE):

        print(f"{FINAL_FILE} not found.")
        return

    df = pd.read_csv(FINAL_FILE)

    llm = APIClient()

    judge = LLMJudge(llm)

    error_rows = df[
        (
            df["judge_explanation"].isna()
        )
        |
        (
            df["judge_explanation"] == "Judge Error"
        )
        |
        (
            df["judge_explanation"] == ""
        )
    ]

    if len(error_rows) == 0:

        print("No judge errors found.")

        return

    print(
        f"Found {len(error_rows)} judge error(s).\n"
    )

    for index, row in error_rows.iterrows():

        print(
            f"Retrying row {row['id'] + 1}..."
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

            df.loc[
                index,
                "judge_explanation"
            ] = result["explanation"]

            print("Success")

        except Exception as e:

            print(f"Failed again: {e}")

        df.to_csv(
            FINAL_FILE,
            index=False
        )

    print()

    print("Finished.")

    print(
        f"Updated {FINAL_FILE}"
    )


if __name__ == "__main__":
    main()