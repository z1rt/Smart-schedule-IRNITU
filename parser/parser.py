import requests
from bs4 import BeautifulSoup

from pprint import pprint

# ССылки для разных источников парсинга
URL_schelude_groups = 'https://www.istu.edu/schedule/default?group=459303'
URL_inst = 'https://www.istu.edu/schedule/'
URL_groups = 'https://www.istu.edu/schedule/?subdiv=683'

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

def inst(html):
    '''Возвращает институты и ссылки на них'''
    soup = BeautifulSoup(html, 'html.parser')
    insts = soup.find(class_='content')
    inst = insts.find_all('li')
    inst_tags_list = []
    links = []
    rd_inst = {}
    rd_inst_list = []
    #Берём названия институтов
    for ins in inst:
        inst_tags_list.append(ins.find('a').text)
    #Берём ссылки
    for link in soup.find_all('a'):
        if '?subdiv' in str(link):
            links.append('https://www.istu.edu/schedule/'+ link.get('href'))


    for i in range(len(inst_tags_list)):
        rd_inst['name'] = inst_tags_list[i]
        rd_inst['link'] = links[i]
        rd_inst_list.append(rd_inst)


    return rd_inst_list



def group(html):
    '''Возвращает группы и ссылки на них'''
    soup = BeautifulSoup(html, 'html.parser')
    groups = soup.find(class_='kurs-list')
    courses = groups.find_all('li')
    links = []
    groups_parse_list = []
    rd_groups = {}
    rd_groups_list = []


    #Получаем ссылки
    for link in soup.find_all('a'):
        if '?group=' in str(link):
            links.append('https://www.istu.edu/schedule/'+ link.get('href'))

    #Получаем курсы
    for i in courses:
        if groups_parse_list == []:
            groups_parse_list.append(i.find('a').text)
        else:
            if i.find('a').text == groups_parse_list[-1]:
                continue
            else:
                groups_parse_list.append(i.find('a').text)

    for i in range(len(groups_parse_list)):
        rd_groups['name'] = groups_parse_list[i]
        rd_groups['link'] = links[i]
        rd_groups_list.append( rd_groups)


    return rd_groups_list



def count_course(html):
    '''Получаем кол-во курсов'''
    soup = BeautifulSoup(html, 'html.parser')
    groups = soup.find(class_='kurs-list')
    count_courses = len(groups.find_all('ul'))
    course = []
    for i in range(1, count_courses + 1):
        course.append("Курс" + " "+ str(i))

    return course


def main():
    html_schelude_groups = get_html(url = URL_schelude_groups)
    html_insts = get_html(url = URL_inst)
    html_groups = get_html(url = URL_groups)
    html_count_groups = get_html(url = URL_groups)
    schedule = get_schedule(html_schelude_groups)
    dict_insts = inst(html_insts)
    dict_groups = group(html_groups)
    course = count_course(html_count_groups)
    pprint(schedule)
    pprint(dict_insts)
    pprint(dict_groups)
    pprint(course)


if __name__ == '__main__':
    main()