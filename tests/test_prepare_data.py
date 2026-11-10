from sklearn.datasets import load_iris
from iris_project.transformers.prepare_data import prepare_data

def test_split_is_80_20():
    df = load_iris(as_frame=True).frame
    out = prepare_data(df)

    assert (out["split"] == "train").sum() == 120
    assert (out["split"] == "test").sum() == 30
