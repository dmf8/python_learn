from config.config import Config
from config.config import Sheet
import pandas as pd
from read.get_dataframe import *
import os


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
    df = filtColumnsPrecisely(df, sheet.columnNames())
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


def checkSheetColumns(sheet: Sheet, df: pd.DataFrame) -> Sheet:
    """check real sheet to correct column names in configurations

    Raise
    """
    sheet2 = sheet
    for i in range(len(sheet2.columns), 0, -1):
        j = i-1
        fuzzy_name = sheet2.columns[j].name
        try:
            check_name = checkColumnName(df, fuzzy_name)
            sheet2.columns[j].name = check_name
        except:
            sheet2.columns.pop(j)
    if len(sheet2.columns) == 0:
        raise Exception(f"empty sheet {sheet2.file} {sheet2.sheet}")
    return sheet2


# main
def main():
    path = "config/config.json"
    config = Config(path)
    for sheet in config.sheets:
        try:
            df = getDataframe(sheet.file, sheet.sheet, sheet.header)
            checked_sheet = checkSheetColumns(sheet, df)
            df = filtColumnsPrecisely(df, checked_sheet.columnNames())
            for column in checked_sheet.columns:
                df = filtCondition(df, column.name, column.condition)
            print(df)
            # # sorting
            # sort_cols = []
            # sort_type = []
            # for column in sheet.columns:
            #     check_type = checkSorting(column.ordering)
            #     if None != check_type:
            #         sort_cols.append(column.name)
            #         sort_type.append(check_type)
            # df = df.sort_values(sort_cols, ascending=sort_type)
            # # finish
            # return df
        except Exception as e:
            print(e)


main()
# df = getDataFrameByConfig(sheet)
# if None != df:
#     dfs.append(df)


# try:
# os.remove("out.xlsx")
# getDataByConfig("config/config.json")
# df = getDataframe("test.xlsx", "Sheet2", 4)
# print(df)
# except Exception as e:
#     print(e)
