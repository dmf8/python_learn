import pandas as pd


def test(path: str):
    data = pd.read_excel(path, sheet_name="Sheet2")
    print(data.describe())
