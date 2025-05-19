import pandas as pd
import re


def getDataframe(file_name, sheet_name, header=0) -> pd.DataFrame:
    df = pd.DataFrame()
    try:
        with open(file_name, "r") as f:
            df = pd.read_excel(file_name, sheet_name, header=header)
    except Exception as e:
        print(f"read error {str(e)}")
    return df


def testColumnName(df: pd.DataFrame, name: str) -> str:
    columns = df.columns
    for c in columns:
        if _matchName(name, c):
            return c
    return ""


def _matchName(name: str, col: str) -> bool:
    match = re.search(name, col)
    if match != None and match.group(0) == col:
        return True
    else:
        return False
