# Задание 2. В приложении парсинга википедии получить первую ссылку на другую страницу и вывести все значимые слова
# из неё. Результат записать в файл в форматированном виде.

import collections
import requests
import re

def return_wiki_html(topic):
    wiki_request = requests.get(f'https://ru.wikipedia.org/wiki/{topic.capitalize()}')
    return wiki_request.text

def main_words_from_link(topic):
    html = return_wiki_html(topic)
    pattern = r'"\/wiki\/[%A-Z0-9_(%A-Z0-9)]*"'
    link = re.search(pattern, html)
    link = link.group()
    link = link.replace('"', '')
    link = 'https://ru.wikipedia.org' + link
    req = requests.get(link)
    html_2 = req.text
    words = re.findall('[а-яА-Я]{3,}', html_2)
    words_counter = collections.Counter()
    for word in words:
        words_counter[word] += 1
    with open("HW_2_output.txt", "w") as file:
        for word in words_counter.most_common(10):
            i = f'Слово {word[0]} встречается {word[1]} раз'
            file.write(str(i) + '\n')
    return file

top_ = 'человек'
main_words_from_link(top_)