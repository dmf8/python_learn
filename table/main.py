from config.config import Config
import pandas as pd

cg = Config("config/config.json")
# cg.output()

df = pd.read_excel("test.xlsx", sheet_name=None)

print(df)
