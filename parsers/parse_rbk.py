# Импорт библиотек
import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd


class RbcParser:
    def __init__(self):
        pass

    def get_search_table(self, param_dict: dict) -> pd.DataFrame:
        """
        Возвращает pd.DataFrame со списком статей

        includeText: bool
        ### Если True, статьи возвращаются с текстами
        """
        soup = bs(rq.get("https://www.rbc.ru/v10/ajax/get-news-by-filters/", param_dict).json()["html"], "lxml")
        return pd.DataFrame([{"title": ' '.join(soupchik.find("span", {"class": "item__title rm-cm-item-text"}).text.split()),
                              "link": soupchik["href"],
                              "text": self.get_article_data(soupchik["href"])}
                             for soupchik in soup.find_all("a", {"class": "item__link"})])

    def get_article_data(self, url: str):
        """
        Возвращает описание и текст статьи по ссылке
        """
        r = rq.get(url)
        soup = bs(r.text, features="lxml")

        return ' '.join(' '.join([i.text for i in soup.find_all('p')]).split())

    def get_articles(self, param_dict) -> pd.DataFrame:
        """
        param_dict: dict
        ### Параметры запроса
        ###### category - категория поиска
        ###### offset - смещение поисковой выдачи
        ###### step - шаг подгрузки, 12
        ###### limit - лимит статей
        """

        offset = param_dict["offset"]
        limit = param_dict["limit"]
        step = param_dict["step"]
        category = param_dict["category"]
        request_params = {
            "limit": step,
            "category": category
            }

        out = pd.DataFrame()

        while offset < limit:
            request_params["offset"] = offset
            print(f'Parsing articles from {offset} to {offset+step}')
            out = pd.concat([out, self.get_search_table(request_params)], ignore_index=True)
            print(f"Total news: {len(out)}")
            offset += step

        print('Finish')

        return out


if __name__ == "__main__":
    # Задаем параметры запросы и складываем в param_dict
    param_dict = \
        {
            'category': 'business',
            'offset': 0,
            'limit': 50,
            'step': 12
        }
    parser = RbcParser()

    for category in ["economics", "business", "finances", "technology_and_media", "politics"]:
        param_dict["category"] = category

        print("param_dict:", param_dict)

        parser.get_articles(param_dict=param_dict).to_csv(f"../parced_data/rbk_{category}.csv")
