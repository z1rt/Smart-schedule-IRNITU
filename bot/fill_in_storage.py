"""Ручное заполнение таблиц"""

from storage import MongodbService
from pprint import pprint

storage = MongodbService()


def test_data():
    pass


test_data()


def full_data():
    storage.save_institutes(
        [{'name': 'Аспирантура'}, {'name': 'Байкальский институт БРИКС'}, {'name': 'ИАиТ'}, {'name': 'ИАСиД'},
         {'name': 'ИВТ'}, {'name': 'Институт заочно-вечернего обучения'}, {'name': 'ИИТиАД'}, {'name': 'ИН'},
         {'name': 'ИЭУиП'}, {'name': 'ИЭ'}])

    storage.save_courses([
        {'name': '1 курс', 'institute': 'ИВТ'},
        {'name': '2 курс', 'institute': 'ИВТ'},
        {'name': '3 курс', 'institute': 'ИВТ'},
        {'name': '4 курс', 'institute': 'ИВТ'},

        {'name': '1 курс', 'institute': 'ИИТиАД'},
        {'name': '2 курс', 'institute': 'ИИТиАД'},
        {'name': '3 курс', 'institute': 'ИИТиАД'},
        {'name': '4 курс', 'institute': 'ИИТиАД'},
        {'name': '5 курс', 'institute': 'ИИТиАД'},
    ])

    storage.save_groups([
        {
            'name': 'ИБб-18-1',
            'institute': 'ИИТиАД',
            'course': '3 курс'
        },
        {
            'name': 'ИБб-18-2',
            'institute': 'ИИТиАД',
            'course': '3 курс'
        },
        {
            'name': 'ИБб-20-1',
            'institute': 'ИИТиАД',
            'course': '1 курс'
        }
    ])
