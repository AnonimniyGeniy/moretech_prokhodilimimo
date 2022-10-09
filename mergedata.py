import json

import pandas as pd

fb = pd.read_csv("parced_data/forbes_data.csv") #1
fbuh = pd.read_csv("parced_data/buh_data.csv") #2
feconomics = pd.read_csv("parced_data/rbk_economics.csv") #1
ffinances = pd.read_csv("parced_data/rbk_finances.csv") #1
fpolitics = pd.read_csv("parced_data/rbk_politics.csv") #3
ftrash = pd.read_csv("parced_data/rbk_technology_and_media.csv") #3

newdata = pd.DataFrame()
newdata["link"] = ""
newdata["title"] = ""
newdata["text"] = ""
newdata["category"] = ""
sp = []

for i in range(len(fb)):
    #print(fb['link'][i])
    sp.append([fb['link'][i], fb['text'][i], fb['title'][i], 1])

for i in range(len(fbuh)):
    #print(fb['link'][i])
    sp.append([fbuh['link'][i], fbuh['text'][i], fbuh['title'][i], 2])

for i in range(len(feconomics)):
    #print(fb['link'][i])
    sp.append([feconomics['href'][i], feconomics['text'][i], feconomics['title'][i], 1])

for i in range(len(ffinances)):
    #print(fb['link'][i])
    sp.append([ffinances['href'][i], ffinances['text'][i], ffinances['title'][i], 1])

for i in range(len(fpolitics)):
    #print(fb['link'][i])
    sp.append([fpolitics['href'][i], fpolitics['text'][i], fpolitics['title'][i], 3])
for i in range(len(ftrash)):
    #print(fb['link'][i])
    sp.append([ftrash['href'][i], ftrash['text'][i], ftrash['title'][i], 3])

newdata = pd.DataFrame(data=sp, columns=["link", "text", "title", "category"])
newdata.to_csv("parced_data/merged_data.csv")