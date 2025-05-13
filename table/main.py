from config.config import Config
import pandas as pd

cg = Config("config/config.json")
# cg.output()

df = pd.read_excel("test.xlsx", sheet_name="Sheet2")

# print(df.info())
# print(df.describe())
# print(df.dtypes)

columns = df.columns

df2 = df.sort_values()
# print(df)
print(df2)
