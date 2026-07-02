import os
import sys
import argparse

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

from agents.semantic_agent import SemanticRiskDetector
from agents.override_agent import OverrideDetector
from agents.leakage_agent import LeakageDetector
from agents.role_hijack_agent import RoleHijackDetector
from agents.benign_validator import BenignIntentValidator


AGENTS = {
    "semantic": (SemanticRiskDetector, "semantic"),
    "override": (OverrideDetector, "override"),
    "leakage": (LeakageDetector, "leakage"),
    "role_hijack": (RoleHijackDetector, "role_hijack"),
    "benign_validator": (BenignIntentValidator, "benign_validator"),
}


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "agent",
        choices=AGENTS.keys()
    )

    args = parser.parse_args()

    detector_class, prefix = AGENTS[args.agent]

    llm = APIClient()

    detector = detector_class(llm)

    output_path = f"results/agents/qwen35_35b_moe/{prefix}.csv"

    if not os.path.exists(output_path):
        print(f"{output_path} not found.")
        return

    df = pd.read_csv(output_path)

    error_column = f"{prefix}_vote"

    error_rows = df[df[error_column] == "error"]

    if len(error_rows) == 0:
        print("No error rows found.")
        return

    print(f"Found {len(error_rows)} error row(s).\n")

    for index, row in error_rows.iterrows():

        print(
            f"Retrying row {row['id'] + 1}..."
        )

        try:

            result = detector.analyze(
                row["prompt"]
            )

            df.loc[index, f"{prefix}_vote"] = result["vote"]
            df.loc[index, f"{prefix}_confidence"] = result["confidence"]
            df.loc[index, f"{prefix}_reason"] = result["reason"]

            print(" Success")

        except Exception as e:

            print(f" Failed again: {e}")

    df.to_csv(
        output_path,
        index=False
    )

    print()
    print("Finished.")
    print(f"Updated {output_path}")


if __name__ == "__main__":
    main()