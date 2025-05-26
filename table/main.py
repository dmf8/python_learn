from config.config import Config
from config.config import Sheet
import pandas as pd
from read.get_dataframe import *


# cg = Config("config/config.json")
# for sheet in cg.sheets:
#     names, ascendings = sheet.getSortings()


def getDataByConfig(path: str):
    config = Config(path)
    dfs: list[pd.DataFrame] = []
    for sheet in config.sheets:
        df = getDataFrameByConfig(sheet)
        if None != df:
            dfs.append(df)
    with pd.ExcelWriter("out.xlsx", engine="openpyxl") as writer:
        i = 0
        for df in dfs:
            df.to_excel(writer, sheet_name=f"Sheet{i}", index=False)
            i += 1


def getDataFrameByConfig(sheet: Sheet) -> pd.DataFrame:
    # check column names
    sheet = checkSheetColumns(sheet)
    df = getDataframe(sheet.file, sheet.sheet, sheet.header)
    # filt by column names
    df = filtColumnsPrecisely(df, sheet.getColumnNames())
    # filt by column conditions
    for column in sheet.columns:
        df = filtCondition(df, column.name, column.condition)
    # sorting
    sort_cols = []
    sort_type = []
    for column in sheet.columns:
        check_type = checkSorting(column.ordering)
        if None != check_type:
            sort_cols.append(column.name)
            sort_type.append(check_type)
    df = df.sort_values(sort_cols, ascending=sort_type)
    # finish
    return df


def checkSheetColumns(sheet: Sheet) -> Sheet:
    df = getDataframe(sheet.file, sheet.sheet, sheet.header)
    for i in range(len(sheet.columns), 0, -1):
        j = i-1
        fuzzy_name = sheet.columns[j].name
        check_name = checkColumnName(df, fuzzy_name)
        if check_name == "":
            sheet.columns.pop(j)
        else:
            sheet.columns[j].name = check_name
    return sheet


# getDataByConfig("config/config.json")

try:
    df = getDataframe("test.xlsx", "Sheet2", 4)
    print(df)
except Exception as e:
    print(e)
