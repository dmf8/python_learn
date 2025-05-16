from config.config import Config
import pandas as pd

cg = Config("config/config.json")
# cg.output()

dfs = pd.read_excel("test.xlsx", None)
df2 = pd.read_excel("test.xlsx", "Sheet2")

print(df2.index)
print(len(df2.index))

print(df2)
print("-------------")
# print(df2[0:5])
# rows = len(df2.index)

# df2.index = range(3, rows+3)
# df2.columns = df2.iloc[1]
# df2.reset_index()
# print(df2)
