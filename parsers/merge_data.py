import os
import pandas as pd

paths = ["../parced_data/" + f for f in os.listdir("../parced_data/")]
print(paths)
df = pd.concat([pd.read_csv(path, index_col=0, sep=",") for path in paths], ignore_index=True)
print(df[["link", "text", "title"]].info())
df[["link", "text", "title"]].to_csv("../merged_data.csv")