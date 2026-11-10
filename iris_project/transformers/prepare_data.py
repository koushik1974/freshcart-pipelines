import pandas as pd
from sklearn.model_selection import train_test_split

try:
    from mage_ai.data_preparation.decorators import transformer, test
except ImportError:
    def transformer(func):
        return func

    def test(func):
        return func

@transformer
def prepare_data(df, *args, **kwargs):
    df = df.dropna()
    train, test_df = train_test_split(
        df, test_size=0.2, random_state=42
    )
    train = train.copy()
    test_df = test_df.copy()
    train["split"] = "train"
    test_df["split"] = "test"
    return pd.concat([train, test_df], ignore_index=True)

@test
def test_output(output, *args):
    assert "split" in output.columns
    assert set(output["split"].unique()) == {"train", "test"}
