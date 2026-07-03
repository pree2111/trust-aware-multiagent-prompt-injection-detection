import os
import sys

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


INPUT_FILE = "results/qwen35_35b_moe/final_results.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    y_true = df["label"]
    y_pred = df["prediction"]

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        pos_label="attack"
    )

    recall = recall_score(
        y_true,
        y_pred,
        pos_label="attack"
    )

    f1 = f1_score(
        y_true,
        y_pred,
        pos_label="attack"
    )

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=["attack", "benign"]
    )

    print("\n========== EVALUATION ==========\n")

    print(f"Total Samples : {len(df)}")
    print(f"Attack Samples: {(y_true == 'attack').sum()}")
    print(f"Benign Samples: {(y_true == 'benign').sum()}")

    print()

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    print("\nConfusion Matrix")
    print("----------------")

    cm_df = pd.DataFrame(
        cm,
        index=[
            "Actual Attack",
            "Actual Benign"
        ],
        columns=[
            "Predicted Attack",
            "Predicted Benign"
        ]
    )

    print(cm_df)

    print("\nClassification Report")
    print("---------------------")

    report = classification_report(
        y_true,
        y_pred,
        digits=4
    )

    print(report)

    print("\nConsensus Distribution")
    print("----------------------")

    print(df["consensus"].value_counts())

    print("\nPrediction Distribution")
    print("-----------------------")

    print(df["prediction"].value_counts())

    print("\nFinal Trust Scores")
    print("------------------")

    trust_columns = [
        "semantic_trust",
        "override_trust",
        "leakage_trust",
        "role_hijack_trust",
        "benign_validator_trust"
    ]

    final = df.iloc[-1]

    for column in trust_columns:
        print(f"{column:<28}{final[column]:.4f}")


    report_file = "results/qwen35_35b_moe/35b_moe_evaluation_report.txt"

    with open(report_file, "w", encoding="utf-8") as f:

        f.write("========== EVALUATION ==========\n\n")

        f.write(f"Total Samples : {len(df)}\n")
        f.write(f"Attack Samples: {(y_true == 'attack').sum()}\n")
        f.write(f"Benign Samples: {(y_true == 'benign').sum()}\n\n")

        f.write(f"Accuracy : {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall   : {recall:.4f}\n")
        f.write(f"F1 Score : {f1:.4f}\n\n")

        f.write("Confusion Matrix\n")
        f.write("----------------\n")
        f.write(cm_df.to_string())

        f.write("\n\nClassification Report\n")
        f.write("---------------------\n")
        f.write(report)

        f.write("\nConsensus Distribution\n")
        f.write("----------------------\n")
        f.write(df["consensus"].value_counts().to_string())

        f.write("\n\nPrediction Distribution\n")
        f.write("-----------------------\n")
        f.write(df["prediction"].value_counts().to_string())

        f.write("\n\nFinal Trust Scores\n")
        f.write("------------------\n")

        for column in trust_columns:
            f.write(f"{column:<28}{final[column]:.4f}\n")


    metrics = pd.DataFrame([
        {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1
        }
    ])

    metrics.to_csv(
    "results/qwen35_35b_moe/evaluation_metrics.csv",
    index=False
)

    print(f"\nSaved evaluation report to {report_file}")
    print("Saved metrics to results/qwen35_35b_moe/evaluation_metrics.csv")


if __name__ == "__main__":
    main()