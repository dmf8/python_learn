import pandas as pd
import re
import operator
import ast


def getDataframe(file_name: str, sheet_name: str, header: int = 0) -> pd.DataFrame:
    """Get DataFrame by file, sheet, and header line"""
    df = pd.DataFrame()
    try:
        with open(file_name, "r") as f:
            df = pd.read_excel(file_name, sheet_name, header=header)
    except Exception as e:
        raise Exception(f"read error: {str(e)}")
    return df


def checkColumnName(df: pd.DataFrame, name: str) -> str:
    columns = df.columns
    for c in columns:
        if _matchName(name, c):
            return c
    return ""


def filtColumnsPrecisely(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    checked_columns = []
    for c in columns:
        if df.columns.__contains__(c):
            checked_columns.append(c)
        else:
            print(f"column name <{c}> not found")
    return df[checked_columns]


def filtColumnsFuzzily(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    checked_columns = checkColumnNames(df, columns)
    return filtColumnsPrecisely(df, checked_columns)


def filtCondition(df: pd.DataFrame, column_name: str, condition: str) -> pd.DataFrame:
    op, data = _parseCondition(condition)
    if op == None:
        return df
    df2 = df.loc[op(df[column_name], data), :]
    return df2


def checkColumnNames(df: pd.DataFrame, columns: list[str]) -> list[str]:
    check_names = []
    for c in columns:
        check = checkColumnName(df, c)
        if check != "":
            check_names.append(check)
        else:
            print(f"column name <{c}> not found")
    return check_names


def _matchName(name: str, col: str) -> bool:
    match = re.search(name, col)
    if match != None and match.group(0) == col:
        return True
    else:
        return False


def _parseCondition(condition: str):
    ops = {
        "==": operator.eq,
        "!=": operator.ne,
        ">=": operator.ge,
        "<=": operator.le,
        ">": operator.gt,
        "<": operator.lt,
    }
    reg = "(==|!=|>=|<=|>|<)(.*)"
    match = re.search(reg, condition)
    if match == None:
        return None, None
    if not (ops.__contains__(match.group(1))):
        return None, None
    op = ops[match.group(1)]
    data = ast.literal_eval(match.group(2))
    print(f"get data {data} of type {type(data)} from condition {condition}")
    return op, data


def checkSorting(sorting: str) -> bool:
    if sorting == "^":
        return True
    elif sorting == "v" or sorting == "V":
        return False
    else:
        return None
