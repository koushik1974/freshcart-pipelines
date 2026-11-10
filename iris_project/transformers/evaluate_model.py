import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def evaluate_model(df, *args, **kwargs):
    y_true = df["target"]
    y_pred = df["prediction"]

    # Confusion matrix
    cm = pd.crosstab(
        y_true,
        y_pred,
        rownames=["Actual"],
        colnames=["Predicted"]
    )
    print("\nConfusion Matrix:")
    print(cm)

    # Metrics table
    metrics = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1-score"],
        "Score": [
            accuracy_score(y_true, y_pred),
            precision_score(y_true, y_pred, average="weighted", zero_division=0),
            recall_score(y_true, y_pred, average="weighted", zero_division=0),
            f1_score(y_true, y_pred, average="weighted", zero_division=0)
        ]
    })

    print("\nMetrics Table:")
    print(metrics.to_string(index=False))

    return metrics

@test
def test_output(output, *args, **kwargs):
    assert output is not None
    assert output["Score"].between(0, 1).all()
