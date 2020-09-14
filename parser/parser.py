import requests
from bs4 import BeautifulSoup

from pprint import pprint

URL = 'https://www.istu.edu/schedule/default?group=459303'


def get_html(url):
    """возвращает страницу по url"""
    response = requests.get(url)
    return response.text


def get_schedule(html):
    """возвращает расписание со страницы html"""
    soup = BeautifulSoup(html, 'html.parser')
    days = soup.find_all(class_='day-heading')
    lines = soup.find_all(class_='class-lines')

    schedule = []

    for line, day in zip(lines, days):
        one_day = {}
        lessons = []
        one_day['day'] = day.text
        tails = line.find_all(class_='class-tails')
        for t in tails:
            time = t.find(class_='class-time').text
            tail = t.find_all(class_='class-tail')
            for item in tail:
                # определяем неделю
                if 'class-even-week' in str(item):
                    week = 'even'
                elif 'class-odd-week' in str(item):
                    week = 'odd'
                else:
                    week = 'all'
                inf = {}
                inf['time'] = time
                inf['week'] = week
                name = item.find(class_='class-pred')
                # смотрим есть ли занятие или свободно
                if not name:
                    inf['name'] = 'свободно'
                else:
                    inf['name'] = name.text
                    inf['aud'] = item.find(class_='class-aud').text
                    inf['info'] = item.find(class_='class-info').text
                    inf['prep'] = item.find('a').text

                lessons.append(inf)
        one_day['lessons'] = lessons
        schedule.append(one_day)

    return schedule


def main():
    html = get_html(url=URL)
    schedule = get_schedule(html)
    pprint(schedule)


if __name__ == '__main__':
    main()
