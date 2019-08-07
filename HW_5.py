# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные объявления с avito.ru в созданную БД (xpath/BS для парсинга на выбор)
# 2) Написать функцию, которая производит поиск и выводит на экран объявления с ценой меньше введенной суммы
# *Написать функцию, которая будет добавлять в вашу базу данных только новые объявления

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def avito_ads():

    url = f'https://www.avito.ru/moskva/zhivotnye'
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36'
    }
    try:
        request = requests.get(url, headers=headers)
        return request.text
    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)

def save_to_mongo():

    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['avito']
    avito_ad = db.avito
    avito_ad.drop()

    soup = BeautifulSoup(avito_ads(), 'html.parser')
    ads = soup.findAll("div", {"class": "description item_table-description"})

    for ad in ads:
        try:
            price = ad.find("div", {"class": "about"}).find("span", {"class": "price"}).string

        except IndexError:
            price = 'Цена не указана'

        ad_data = {
            "title": ad.find("span", {"itemprop": "name"}).string,
            "division": ad.find("div", {"class": "data"}).find("p").string,
            "price": price
        }
        avito_ad.insert_one(ad_data)

if __name__ == '__main__':
   save_to_mongo()
