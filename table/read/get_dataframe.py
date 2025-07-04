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
        if _matchAll(c, name):
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
            print(f"{__name__} error: {e}")
    return check_names


def filtColumnsPrecisely(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """filt DataFrame by given columns"""
    checked_columns = []
    for c in columns:
        if df.columns.__contains__(c):
            checked_columns.append(c)
        else:
            print(f"{__name__} column name <{c}> not found")
    return df[checked_columns]


def fillEmpty(df: pd.DataFrame, column: str, fill: bool) -> pd.DataFrame:
    if not fill:
        return df
    else:
        df[column] = df[column].ffill()
        return df


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
        df2 = df[op(df[column_name], data)]
        return df2
    except Exception as e:
        print(f"{__name__} error: {e}")
        return df


def _matchAll(target: str | pd.Series, pattern: str) -> bool | list[bool]:
    """try to match target with regexp pattern"""
    if isinstance(target, str):
        match = re.search(pattern, target)
        if match != None and match.group(0) == target:
            return True
        else:
            return False
    else:
        ret = []
        for t in target:
            ret.append(_matchAll(t, pattern))
        return ret


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
