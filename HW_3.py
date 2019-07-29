# 1) Необходимо собрать информацию о вакансиях на должность программиста или разработчика с сайта job.ru или hh.ru.
# (Можно с обоих сразу) Приложение должно анализировать несколько страниц сайта.
# Получившийся список должен содержать в себе:
#
# *Наименование вакансии,
# *Предлагаемую зарплату
# *Ссылку на саму вакансию
# 2) Доработать приложение таким образом, чтобы можно было искать разработчиков на разные языки программирования
# (Например Python, Java, C++)

import requests
from lxml import html

def request_to_site(job_title, language):

    url = 'https://hh.ru/search/vacancy'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/53.0.2785.143 Safari/537.36'
    }

    try:
        request = requests.get(url,
                               params={'text': job_title + ' ' + language},
                               headers=headers,
                               timeout=5)
        root = html.fromstring(request.text)

        results_list = root.xpath(".//div[contains(@class, 'item__row_header')]")

        if results_list:
            with open('HW_3_output.txt', 'w') as file:
                for result in results_list:
                    job_ = result.xpath('.//a/text()')[0]
                    link_ = result.xpath('.//a/@href')[0]
                    try:
                        wage_ = result.xpath('.//div[contains(@class, "item__compensation")]/text()')[0]
                    except IndexError:
                        wage_ = '"зарплата не указана"'
                    file.write(f'Найдена вакансия "{job_}" с зарплатой {wage_}' + '\n' +
                               f'ссылка на вакансию {link_}' + '\n' + '-'*100 + '\n')
        else:
            print("At your request no results were found. Please, check your request.")
            request_to_site(job_title, language)
    except requests.exceptions.ConnectionError:
        print("No connection to site")
        exit(1)

job_title = 'программист'
language = 'Python'

if __name__ == '__main__':
   request_to_site(job_title, language)