import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

df = pd.read_excel("csv_to_excel_20260714_153738.xlsx")
print(df)
df = pd.read_excel("csv_to_excel_20260714_153738.xlsx"
	,sheet_name="国語でソート")
print(df)