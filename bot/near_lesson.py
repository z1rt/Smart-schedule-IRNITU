from datetime import datetime
import pytz

TZ_IRKUTSK = pytz.timezone('Asia/Irkutsk')


def get_near_lesson(lessons: list) -> dict:
    '''Возвращает ближайшую пару'''
    global TZ_IRKUTSK

    # ============== тестовые данные =============
    # lessons = [{'date': '3 сентября', 'time': '16:00', 'name': 'Физика', 'aud': 'К-313'},
    #            {'date': '3 сентября', 'time': '17:00', 'name': 'Матан', 'aud': 'Ж-310'}]
    # =============================================

    months = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
              'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}
    year_now = int(datetime.now(TZ_IRKUTSK).strftime('%Y'))
    month_now = int(datetime.now(TZ_IRKUTSK).strftime('%m'))
    day_now = int(datetime.now(TZ_IRKUTSK).strftime('%d'))
    h = int(datetime.now(TZ_IRKUTSK).strftime('%H'))
    m = int(datetime.now(TZ_IRKUTSK).strftime('%M'))
    now = datetime(year_now, month_now, day_now, h, m)

    near_lesson = {'time': '00:00', 'name': '', 'aud': ''}

    last_range = datetime(9999, month_now, day_now, h, m) - datetime(1, month_now, day_now, h, m)
    for les in lessons:
        date = les['date'].split()
        month = months[date[1]]
        day = int(date[0])
        hour, minute = map(int, les['time'].split(':'))
        time = datetime(year=year_now, month=month, day=day, hour=hour, minute=minute)

        if int(month) != int(month_now) or int(month) == int(month_now) and int(day) != int(day_now):
            continue
        range = time - now
        if now <= time and range < last_range:
            last_range = range
            near_lesson['time'] = f'{hour}:{minute}'
            near_lesson['name'] = les['name']
            near_lesson['aud'] = les['aud']

    if not near_lesson['name']:
        near_lesson = {}
    return near_lesson


if __name__ == '__main__':
    app.run()
