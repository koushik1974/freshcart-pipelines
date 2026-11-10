import os
import joblib
from sklearn.tree import DecisionTreeClassifier

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def train_model(df, *args, **kwargs):
    max_depth = kwargs.get("max_depth", 3)

    train = df[df["split"] == "train"]
    test_df = df[df["split"] == "test"].copy()

    X_train = train.drop(columns=["target", "split"])
    y_train = train["target"]
    X_test = test_df.drop(columns=["target", "split"])

    model = DecisionTreeClassifier(
        max_depth=int(max_depth),
        random_state=42
    )
    model.fit(X_train, y_train)

    test_df["prediction"] = model.predict(X_test)
    joblib.dump(model, "/content/iris_project/iris_model.pkl")

    accuracy = (test_df["prediction"] == test_df["target"]).mean()
    print(f"max_depth: {max_depth}")
    print(f"test_accuracy: {accuracy:.4f}")

    return test_df

@test
def test_output(output, *args, **kwargs):
    accuracy = (output["prediction"] == output["target"]).mean()
    assert accuracy >= 0.8, f"Accuracy too low: {accuracy:.4f}"
