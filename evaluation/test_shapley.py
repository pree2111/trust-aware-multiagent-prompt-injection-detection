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

from coalition.shapley import (
    Shapley
)

df = pd.read_csv(
    "results/qwen2.5_3b/results.csv"
)

calculator = (
    Shapley()
)

values = calculator.calculate(
    df
)

print()

print(
    "===== SHAPLEY VALUES ====="
)

print()

for agent, value in sorted(
    values.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        f"{agent}: {value:.4f}"
    )
shapley_df = pd.DataFrame(
    [
        {
            "agent": agent,
            "shapley": value
        }
        for agent, value in sorted(
            values.items(),
            key=lambda x: x[1],
            reverse=True
        )
    ]
)

shapley_df.to_csv(
    "results/qwen2.5_3b/shapley_values.csv",
    index=False
)

print()
print(
    "Shapley values saved to results/shapley_values.csv"
)