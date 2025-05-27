import pandas as pd
import re
import operator
import ast
from typing import Callable
from typing import Any


def getDataframe(file_name: str, sheet_name: str, header: int = 0) -> pd.DataFrame:
    """Get DataFrame by file, sheet, and header line

    Raise
    """
    with open(file_name, "r") as f:
        df = pd.read_excel(file_name, sheet_name, header=header)
        return df


def checkColumnName(df: pd.DataFrame, name: str) -> str:
    """get precise column name by fuzzy name

    Raise
    """
    columns = df.columns
    for c in columns:
        if _matchAll(name, c):
            return c
    raise Exception(f"column {name} not found")


def checkColumnNames(df: pd.DataFrame, columns: list[str]) -> list[str]:
    """get precise column names by fuzzy names"""
    check_names = []
    for c in columns:
        try:
            check = checkColumnName(df, c)
            check_names.append(check)
        except Exception as e:
            print(e)
    return check_names


def filtColumnsPrecisely(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """filt DataFrame by given columns"""
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
    """filt rows by single column condition"""
    if "" == condition:
        return df
    print(f"condition {condition} of {column_name}")
    try:
        op, data = _parseCondition(condition)
        print(op)
        print(f"data {data} {type(data)}")
        df = df.loc[op(df[column_name], data), :]
        print(df)
        return df
    except Exception as e:
        print(e)
        return df


def _matchAll(pattern: str, target: str) -> bool:
    match = re.search(pattern, target)
    if match != None and match.group(0) == target:
        return True
    else:
        return False


def _parseCondition(condition: str) -> tuple[Callable[[Any, Any], bool], Any]:
    """parse condition string to get operation function and data

    Raise
    """
    ops = {
        "reg:": _matchAll,
        "==": operator.eq,
        "!=": operator.ne,
        ">=": operator.ge,
        "<=": operator.le,
        ">": operator.gt,
        "<": operator.lt,
    }
    reg = "(reg:|==|!=|>=|<=|>|<)(.*)"
    match = re.search(reg, condition)
    if match == None:
        raise Exception(f"unknown condition")
    if not (ops.__contains__(match.group(1))):
        raise Exception(f"unknown condition2")
    op = ops[match.group(1)]
    print(match.group(2))
    data = ast.literal_eval(match.group(2))
    return op, data


def checkSorting(sorting: str) -> bool:
    if sorting == "^":
        return True
    elif sorting == "v" or sorting == "V":
        return False
    else:
        return None
