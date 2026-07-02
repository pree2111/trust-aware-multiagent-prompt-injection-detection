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

from coalition.shapley import Shapley


INPUT_FILE = "results/qwen35_122b/merged_results.csv"
OUTPUT_FILE = "results/qwen35_122b/shapley_values.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    shapley = Shapley()

    values = shapley.calculate(df)

    print("\n===== SHAPLEY VALUES =====\n")

    for agent, value in sorted(
        values.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        print(
            f"{agent:<20}"
            f"{value:.4f}"
        )

    pd.DataFrame(
        {
            "agent": values.keys(),
            "shapley_value": values.values()
        }
    ).to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()

    print(
        f"Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()