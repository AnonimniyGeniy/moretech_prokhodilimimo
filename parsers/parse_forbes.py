import time
import requests
import json
import os
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_page_soup_selenium(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        driver.get(url=url)
        time.sleep(1)
        elem = driver.find_element(By.TAG_NAME, "body")
        print(elem)
        no_of_pagedowns = 50
        for _ in range(no_of_pagedowns):
            elem.send_keys(Keys.PAGE_UP)
            time.sleep(0.1)
            elem.send_keys(Keys.END)
            time.sleep(0.2)
        html = driver.page_source

        soup = BeautifulSoup(html, 'lxml')

    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()

def get_links(soup):
    news_links = soup.find_all('a')
    links_array = []
    for i in range(len(news_links)):
        link = news_links[i].get('href').split('?')[0]
        if link[0] != 'h' and len(link) >= 18 and '@' not in link:
            links_array.append('https://www.forbes.ru' + link)
    return links_array

def get_soup(url):
    r = requests.get(url).text
    return BeautifulSoup(r, 'lxml')

def main():
    url = 'https://www.forbes.ru/biznes'
    soup = get_page_soup_selenium(url)

    news_data = {}

    for link in links_array:
        name = link
        news_data[name] = {}
        soup = get_soup(link)
        # print(soup.text)

        # Переходим на страницу для дальнейшенго парсинга
        article = soup.find_all(attrs={'itemprop': 'articleBody'})

        title = soup.title
        article_text = ''
        try:
            article_text = " ".join(paragraph.get_text() for paragraph in article)

        except AttributeError:
            continue

        # print(article_text)

        """for paragraph in article_paragraphs:
            #article_text += paragraph.text
            article_text += paragraph
            print(paragraph)
        print(article_text)"""

        # Заполняем полученными данными news_data
        news_data[name]['link'] = link
        # news_data[name]['date'] = date
        news_data[name]['text'] = ' '.join(article_text.split())

        try:
            news_data[name]['title'] = title.text
        except AttributeError:
            news_data[name]['title'] = 'Без заголовка'

    pd.DataFrame(news_data).transpose().reset_index(drop=True).to_csv("parced_data/forbes_data.csv")


if __name__ == "__main__":
    main()
