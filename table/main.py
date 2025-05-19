from config.config import Config
import pandas as pd
from read.get_dataframe import *

# cg = Config("config/config.json")
# cg.output()


df = getDataframe("test.xlsx", "Sheet2", 3)


col_name = testColumnName(df, "g")
print(f"test name {col_name}")

# dfs = pd.read_excel("test.xlsx", None)
# df2 = pd.read_excel("test.xlsx", "Sheet3")

# print(df2.index)
# print(len(df2.index))

# print(df2)
# print("-------------")
# print(df2[0:5])
# rows = len(df2.index)

# df2.index = range(3, rows+3)
# df2.columns = df2.iloc[1]
# df2.reset_index()
# print(df2)
