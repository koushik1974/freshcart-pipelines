
import pandas as pd
from sklearn.datasets import load_iris

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    iris = load_iris(as_frame=True)
    df = iris.frame
    print("Rows loaded:", len(df))
    return df


@test
def test_output(output, *args):
    assert output is not None, "No data loaded"
    assert len(output) == 150, "Iris must have 150 rows"
