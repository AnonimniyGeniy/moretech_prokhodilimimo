import json

import pandas as pd

fb = pd.read_csv("forbes_data.csv")
fbuh = pd.read_csv("buh_data.csv")
frbk = pd.read_csv("forbes_data.csv")

newdata = pd.DataFrame()
newdata["link"] = ""
newdata["title"] = ""
newdata["text"] = ""
newdata["category"] = ""
for i in fb:
    newdata["link"] = i["link"]
    newdata["text"] = i["text"]
    newdata["title"] = i["title"]
    newdata["cat"] = 1
newdata.to_csv(open("merged_data"))