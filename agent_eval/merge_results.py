import os
import pandas as pd


RESULTS_DIR = "results/agents/qwen35_35b"

FILES = {
    "semantic": "semantic.csv",
    "override": "override.csv",
    "leakage": "leakage.csv",
    "role_hijack": "role_hijack.csv",
    "benign_validator": "benign_validator.csv",
}


def load(name):

    path = os.path.join(
        RESULTS_DIR,
        FILES[name]
    )

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    return pd.read_csv(path)


def main():

    semantic = load("semantic")

    merged = semantic

    for name in [
        "override",
        "leakage",
        "role_hijack",
        "benign_validator"
    ]:

        df = load(name)

        merged = merged.merge(
            df,
            on=[
                "id",
                "prompt",
                "label"
            ],
            how="inner"
        )

    output_path = "results/qwen35_35b/merged_results.csv"

    merged.to_csv(
        output_path,
        index=False
    )

    print()

    print(f"Saved merged file to {output_path}")

    print()

    print(merged.head())


if __name__ == "__main__":
    main()