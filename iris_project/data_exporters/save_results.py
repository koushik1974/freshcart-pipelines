
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

OUTPUT_PATH = "/content/iris_project/iris_predictions.csv"

@data_exporter
def save_results(df, *args, **kwargs):
    df.to_csv(OUTPUT_PATH, index=False)
    print("Predictions saved:", OUTPUT_PATH)

@test
def test_output(*args, **kwargs):
    assert os.path.exists(OUTPUT_PATH), "CSV file was not created"
