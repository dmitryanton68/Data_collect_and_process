# Создать приложение, которое будет из готового файла с данными «Сбербанка»
# (https://www.sberbank.com/ru/analytics/opendata) выводить результат по параметрам:
# • Тип данных
# • Интервал дат
# • Область
# Визуализировать выводимые данные с помощью графика

import csv
from pymongo import MongoClient
import matplotlib.pyplot as plt

file_ = 'opendata.csv'

r = 'Ульяновская область'
n = 'Средняя зарплата'
date_from = '2017-01-01'
date_to = '2017-12-31'

def stat_data(file, name_, region_, d1, d2):

    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client['hw_7_report']
    report = db.hw_7_report
    report.drop()
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['name'] == name_ and row['region'] == region_ and d1 <= row['date'] <= d2:
                doc_data = {
                    'тип данных': name_,
                    'дата': row['date'],
                    'область': region_,
                    'значение': row['value']
                }
                report.insert_one(doc_data)
    return db

def data_output(db):
    money = []
    date = []
    print(f"За период с {date_from} по {date_to} \n по региону {r} \n есть {db.hw_7_report.count()} "
          f"стат. данных \n по параметру '{n.lower()}':")
    print('-'*30)
    for item in db.hw_7_report.find():
        print(f"{item['дата'][:4]}/{item['дата'][5:7]} - {item['значение']} руб.")
        date.append(item['дата'])
        money.append(int(item['значение']))
    print('-'*30)
    return date, money

def imagination(date, money):
    plt.plot(date, money)
    plt.title(f"Данные по региону '{r}' \n за период c {date_from} gо {date_to} \n по параметру '{n.lower()}'")
    plt.xlabel('дата')
    plt.ylabel('руб.')
    plt.xticks(rotation=45)
    plt.show()

dd = data_output(stat_data(file_, n, r, date_from, date_to))
imagination(dd[0],dd[1])
