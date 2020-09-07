from telebot import types
import json

MAX_CALLBACK_RANGE = 41


# Создаём основные кнопки
def make_keyboard_start_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Расписание')
    btn2 = types.KeyboardButton('Ближайшая пара')
    btn3 = types.KeyboardButton('Напоминания')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


# Кнопки выбора института
def make_inline_keyboard_choose_institute(institutes=[]):
    markup = types.InlineKeyboardMarkup()
    for institute in institutes:
        name = institute['name']
        short_name = name

        # Проверяем длину callback_data
        callback_body = '{"institute": ""}'
        if len(name + callback_body) > MAX_CALLBACK_RANGE:
            short_name = name[:MAX_CALLBACK_RANGE - len(callback_body)]

        data = '{"institute": "' + short_name + '"}'

        markup.add(types.InlineKeyboardButton(text=name, callback_data=data))
    return markup


# Кнопки выбора курса
def make_inline_keyboard_choose_courses(courses=[]):
    markup = types.InlineKeyboardMarkup()
    for course in courses:
        name = course['name']
        data = json.dumps({"course": name})
        markup.add(types.InlineKeyboardButton(text=name, callback_data=data))

    # Кнопка назад
    data = json.dumps({"course": "back"})
    markup.add(types.InlineKeyboardButton(text='<', callback_data=data))
    return markup


# Кнопки выбора группы
def make_inline_keyboard_choose_groups(groups=[]):
    markup = types.InlineKeyboardMarkup()
    for group in groups:
        name = group['name']
        data = json.dumps({"group": name})
        markup.add(types.InlineKeyboardButton(text=name, callback_data=data))
    # Кнопка назад
    data = json.dumps({"group": "back"})
    markup.add(types.InlineKeyboardButton(text='<', callback_data=data))
    return markup


# Кнопка "Настройка уведомлений"
def make_inline_keyboard_notifications(time=0):
    markup = types.InlineKeyboardMarkup()
    data = json.dumps({"notification_btn": time})
    markup.add(types.InlineKeyboardButton(text='Настройки ⚙', callback_data=data))
    data = json.dumps({"notification_btn": "close"})
    markup.add(types.InlineKeyboardButton(text='Свернуть', callback_data=data))
    return markup


# Кнопки настройки уведомлений
def make_inline_keyboard_set_notifications(time=0):
    markup = types.InlineKeyboardMarkup()
    data_del = json.dumps({"del_notifications": time})
    if time != 0:
        text_check = f'{time} мин'
    else:
        text_check = 'off'
    data_add = json.dumps({"add_notifications": time})
    markup.add(types.InlineKeyboardButton(text='-', callback_data=data_del),
               types.InlineKeyboardButton(text=text_check, callback_data='None'),
               types.InlineKeyboardButton(text='+', callback_data=data_add))
    # Кнопка Сохранить
    data_save = json.dumps({"save_notifications": time})
    markup.add(types.InlineKeyboardButton(text='Сохранить', callback_data=data_save))
    return markup
