# Задание 1. Доработать приложение по поиску авиабилетов, чтобы оно возвращало билеты по названию города,
# а не по IATA коду. Пункт отправления и пункт назначения должны передаваться в качестве параметров.
# Сделать форматированный вывод, который содержит в себе пункт отправления, пункт назначения, дату вылета,
# цену билета (можно добавить еще другие параметры по желанию)

import requests, pprint, sys

from_ = sys.argv[1]
to_ = sys.argv[2]

def city_code(from_, to_):

    param = {
        'q': from_ + ' ' + to_
    }

    r = requests.get("https://www.travelpayouts.com/widgets_suggest_params", params=param)
    r_data = r.json()

    return r_data


def tickets(origin, destination):

    flight_params = {
    'origin': origin,
    'destination': destination
    }

    r = requests.get("http://min-prices.aviasales.ru/calendar_preload", params=flight_params)
    r_data = r.json()

    return r_data['best_prices']

cod = city_code(from_, to_)
origin = cod['origin']['iata']
destination = cod['destination']['iata']

lst = tickets(origin, destination)

for i in range(len(lst)-1):
    print(f"{i + 1}. Самолёт из г.{from_} в г.{to_} на {lst[i]['depart_date']} стоимость билета {lst[i]['value']} руб.")


