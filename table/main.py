from config.config import Config
from config.config import Sheet
import pandas as pd
from read.get_dataframe import *
import os
import operator
import argparse

parser = argparse.ArgumentParser(
    description="excel data reader by configurations"
)
parser.add_argument("config", help="configuration file",
                    default="config.json", nargs="?")
args = parser.parse_args()
print(args.config)


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
        raise Exception(f"empty sheet: {sheet2.file}/{sheet2.sheet}")
    return sheet2


# main
def main():
    config = Config(args.config)
    for sheet in config.sheets:
        try:
            df = getDataframe(sheet.file, sheet.sheet, sheet.header)
            checked_sheet = checkSheetColumns(sheet, df)
            df = filtColumnsPrecisely(df, checked_sheet.columnNames())
            for column in checked_sheet.columns:
                df = filtCondition(df, column.name, column.condition)
            sort_cols, sort_types = sheet.sortings()
            df = df.sort_values(sort_cols, ascending=sort_types)
            print(df)
        except Exception as e:
            print(f"get sheet {sheet.file}/{sheet.sheet} with error: {e}")


main()
