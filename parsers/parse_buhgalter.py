import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_soup(url: str, params: dict = dict()):
    r = requests.get(url, params)
    r.encoding = r.apparent_encoding
    if r.status_code != 200:
        raise Exception()
    return BeautifulSoup(r.text, "lxml")

def get_page_links(rubric_url):
    soup = get_soup(rubric_url)
    return [{"rubric": rubric_url.split("/")[-2], "href": j["href"], "title": j.text}
            for j in [i.find("a") for i in soup.find_all("h3")]
            if "article" in j["href"]]

def get_all_article_links(main_page_url):
    soup = get_soup(main_page_url)
    categories = [i["href"] for i in soup.find("ul", {"class": "dropnav-menu"}).find_all("a")]
    categories = [href for href in categories if "rubric" in href]

    all_page_links = list()
    all_page_hrefs = set()
    for rubric in categories:
        page_links = get_page_links(rubric_url=rubric)
        for link in page_links:
            link["href"] = link["href"].split("?")[0]
            if main_page_url not in link["href"]:
                link["href"] = main_page_url + link["href"]
            if link["href"] not in all_page_hrefs:
                all_page_hrefs.add(link["href"])
                all_page_links.append(link)
    return all_page_links


def main():
    """
    Parses last news and writes them to csv "buh_data.csv"
    :return:
    """
    url = 'https://www.buhgalteria.ru'
    all_pages = get_all_article_links(url)
    news_data = {}

    # Для каждой ссылки получаем информацию и записываем в news_data
    for page in all_pages:

        link = page["href"]
        name = link
        news_data[name] = {"title": page["title"], "category": page["rubric"], "link": link}
        soup = get_soup(link)

        # Переходим на страницу для дальнейшенго парсинга
        article = soup.find('div', class_='article')

        article_text = " ".join(art.text for art in article.find_all('p'))

        # Заполняем полученными данными news_data
        news_data[name]['text'] = " ".join(article_text.split())

    pd.DataFrame(news_data).transpose().reset_index(drop=True).to_csv("../parced_data/buh_data.csv")


if __name__ == "__main__":
    main()