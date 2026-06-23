import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

df = pd.read_csv(
    "results/qwen2.5_3b/results.csv"
)

y_true = df["label"]

y_pred = df["prediction"]

print("\n===== METRICS =====\n")

print(
    "Accuracy:",
    accuracy_score(
        y_true,
        y_pred
    )
)

print(
    "Precision:",
    precision_score(
        y_true,
        y_pred,
        pos_label="attack"
    )
)

print(
    "Recall:",
    recall_score(
        y_true,
        y_pred,
        pos_label="attack"
    )
)

print(
    "F1:",
    f1_score(
        y_true,
        y_pred,
        pos_label="attack"
    )
)

print("\n===== CONFUSION MATRIX =====\n")

print(
    confusion_matrix(
        y_true,
        y_pred,
        labels=[
            "attack",
            "benign"
        ]
    )
)

print("\n===== CLASSIFICATION REPORT =====\n")

print(
    classification_report(
        y_true,
        y_pred
    )
)
errors = df[
    df["correct"] == False
]

errors.to_csv(
    "results/qwen2.5_3b/errors.csv",
    index=False
)

print(
    f"Errors: {len(errors)}"
)
agents = [
    "semantic",
    "override",
    "leakage",
    "role_hijack",
    "benign_validator"
]

for agent in agents:

    accuracy = (
        df[f"{agent}_vote"]
        ==
        df["label"]
    ).mean()

    print(
        f"{agent}: {accuracy:.4f}"
    )
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

report = classification_report(
    y_true,
    y_pred
)

false_negatives = (
    (
        df["label"] == "attack"
    )
    &
    (
        df["prediction"] == "benign"
    )
).sum()

false_positives = (
    (
        df["label"] == "benign"
    )
    &
    (
        df["prediction"] == "attack"
    )
).sum()
with open(
    "results/metrics.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "===== METRICS =====\n\n"
    )

    f.write(
        f"Accuracy: {accuracy}\n"
    )

    f.write(
        f"Precision: {precision}\n"
    )

    f.write(
        f"Recall: {recall}\n"
    )

    f.write(
        f"F1: {f1}\n\n"
    )

    f.write(
        "===== CONFUSION MATRIX =====\n\n"
    )

    f.write(
        str(cm)
    )

    f.write("\n\n")

    f.write(
        f"False Positives: {false_positives}\n"
    )

    f.write(
        f"False Negatives: {false_negatives}\n\n"
    )

    f.write(
        "===== CLASSIFICATION REPORT =====\n\n"
    )

    f.write(report)