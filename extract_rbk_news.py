import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd

class rbc_parser:
    def __init__(self):
        pass

    def get_search_table(self, param_dict: dict,
                         include_text: bool = True) -> pd.DataFrame:
        """
        Возвращает pd.DataFrame со списком статей

        includeText: bool
        ### Если True, статьи возвращаются с текстами
        """

        r = rq.get("https://www.rbc.ru/v10/search/ajax/", param_dict)
        search_table = pd.DataFrame(r.json()['items'])
        if include_text and not search_table.empty:
            get_text = lambda x: self.get_article_data(x['fronturl'])
            search_table[['overview', 'text']] = search_table.apply(get_text,
                                                                    axis=1).tolist()
        search_table["publish_date_t"] = search_table["publish_date_t"].astype(int)
        return search_table.sort_values('publish_date_t', ignore_index=True)


    def get_article_data(self, url: str):
        """
        Возвращает описание и текст статьи по ссылке
        """
        r = rq.get(url)
        soup = bs(r.text, features="lxml") # features="lxml" чтобы не было warning
        div_overview = soup.find('div', {'class': 'article__text__overview'})

        overview = None
        text = None

        if div_overview:
            overview = div_overview.text.replace('<br />','\n').strip()
        p_text = soup.find_all('p')
        if p_text:
            text = ' '.join(map(lambda x:
                                x.text.replace('<br />','\n').strip(),
                                p_text))

        return overview, text

    def get_articles(self, param_dict) -> pd.DataFrame:
        """
        Функция для скачивания статей интервалами через каждые time_step дней
        Делает сохранение таблицы через каждые save_every * time_step дней

        param_dict: dict
        ### Параметры запроса
        ###### project - раздел поиска, например, rbcnews
        ###### category - категория поиска, например, TopRbcRu_economics
        ###### dateFrom - с даты
        ###### dateTo - по дату
        ###### offset - смещение поисковой выдачи
        ###### limit - лимит статей, максимум 100
        ###### query - поисковой запрос (ключевое слово), например, РБК
        """

        offset = param_dict["offset"]
        limit = param_dict["limit"]
        step = 10
        request_params = param_dict.copy()
        request_params["limit"] = step

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
    param_dict = {'query'   : 'РБК',
                'project' : 'rbcnews',
                'category': 'TopRbcRu_economics',
                'offset'  : 0,
                'limit'   : 200,
                'material': ''}


    print("param_dict:", param_dict)

    parser = rbc_parser()
    tbl = parser.get_search_table(param_dict,
                                  include_text=True) # Парсить текст статей

    # Пример работы программы итеративного сбора большого количества текстов статей
    # Работает, конечно, очень долго :(
    table = parser.get_articles(param_dict=param_dict)
    table.to_csv("rbk_last_news.csv")