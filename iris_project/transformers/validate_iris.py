
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def validate_iris(df, *args, **kwargs):
    missing_values = df.isnull().sum().sum()
    number_of_classes = df["target"].nunique()

    print("Missing values:", missing_values)
    print("Number of classes:", number_of_classes)

    return df

@test
def test_output(output, *args, **kwargs):
    assert output.isnull().sum().sum() == 0, "Dataset contains missing values"
    assert output["target"].nunique() == 3, "Expected exactly 3 classes"
