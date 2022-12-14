import json
import random
import pandas as pd


if __name__ == "__main__":
    try:
        from pipeline import TextPipeline
        pipe = TextPipeline.TextProcessingPipeline("../pipeline/model.pt", 'cpu')
    except Exception as e:
        pipe = lambda x: ("Empty", random.random(), random.random(), 0.0)
    df = pd.read_csv("../merged_data.csv", index_col=0)
    count = 0
    items = list()
    for i in range(len(df)):
        if type(df["title"][i]) is float:
            continue

        count += 1
        summary, economist, director, trash = pipe(df["text"][i])
        items.append(dict(href=df["link"][i], title=df["title"][i], text=summary, relevant={"buh": economist, "dir": director, "trash": trash}))

    with open("../front/data/done_data.json", "w", encoding="utf-8") as file:
        json.dump({"count": count, "items": items}, file, ensure_ascii=False, indent=4)