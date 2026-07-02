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

    df = pd.read_csv(
        "data/prompt_injection_dataset.csv"
    )

    os.makedirs(
        "results/agents/qwen35_122b",
        exist_ok=True
    )

    output_path = f"results/agents/qwen35_122b/{prefix}.csv"



    if os.path.exists(output_path):

        existing = pd.read_csv(output_path)

        results = existing.to_dict("records")

        start = len(existing)

        print(f"Resuming from row {start + 1}")

    else:

        results = []

        start = 0

    total = len(df)


    for i, row in enumerate(
        df.iloc[start:].itertuples(index=False),
        start=start
    ):

        print(f"{prefix}: {i+1}/{total}")

        try:

            result = detector.analyze(
                row.prompt
            )

        except Exception as e:

            print(f"ERROR on row {i+1}: {e}")

            result = {
                "vote": "error",
                "confidence": 0.0,
                "reason": str(e)
            }

        results.append(
            {
                "id": i,
                "prompt": row.prompt,
                "label": row.label,

                f"{prefix}_vote":
                    result["vote"],

                f"{prefix}_confidence":
                    result["confidence"],

                f"{prefix}_reason":
                    result["reason"]
            }
        )


        pd.DataFrame(results).to_csv(
            output_path,
            index=False
        )

    print()

    print("Finished.")

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()