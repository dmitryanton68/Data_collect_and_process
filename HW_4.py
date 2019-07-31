# 1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
#
# *Заголовок
# *Краткое описание
# *Ссылка на новость
# 2) * Разбить новости по категориям
# * Расположить в хронологическом порядке


import requests
from bs4 import BeautifulSoup
from datetime import time

def news_from_yandex(city):

    url = f'https://news.yandex.ru/{city}'

    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36'
    }

    try:
        request = requests.get(url,
                               headers=headers)
        html_doc = request.text

        soup = BeautifulSoup(html_doc, 'html.parser')

        news_ = soup.findAll("div", {"class": "story story_view_normal"}, limit=10)

        if news_:
            with open('HW_4_output.txt', 'w') as file:
                for new_ in news_:
                    title_ = new_.find("h2", {"class": "story__title"}).string
                    content_= new_.find("div", {"class": "story__text"}).string
                    link_ = "https://news.yandex.ru" + new_.find("h2", {"class": "story__title"}).find("a")['href']
                    datetime_ = new_.find("div", {"class": "story__info"}).string
                    tm_ = time(int(datetime_.split(' ')[2].split('\n')[1].split(':')[0]),
                              int(datetime_.split(' ')[2].split('\n')[1].split(':')[1]))
                    file.write(f'{title_} \n' + f'{content_} \n' + f'{link_} \n' + f'{tm_} \n' + '-' * 100 + '\n')

        else:
            print("At your request no results were found. Please, check your request.")
            news_from_yandex(city)

    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)

city = 'Moscow'

if __name__ == '__main__':
   news_from_yandex(city)