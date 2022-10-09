import os
import pandas as pd

paths = ["../parced_data/" + f for f in os.listdir("../parced_data/")]
df = pd.concat([pd.read_csv(path, index_col=0, usecols=["link", "text", "title"]) for path in paths], ignore_index=True)
df.to_csv("../parced_data/merged_data.csv")