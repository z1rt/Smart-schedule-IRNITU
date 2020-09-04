from telebot import types
import json


# Создаём основные кнопки
def makeReplyKeyboard_startMenu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn1 = types.KeyboardButton('Расписание')
    btn2 = types.KeyboardButton('Ближайшая пара')
    btn3 = types.KeyboardButton('Напоминания')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


# Кнопки выбора института
def makeInlineKeyboard_chooseInstitute(institutes=[]):
    print(institutes)
    markup = types.InlineKeyboardMarkup()
    for institute in institutes:
        name = institute['name']
        data = json.dumps({"institute": name})
        markup.add(types.InlineKeyboardButton(text=name, callback_data=data))
    return markup


# Кнопки выбора курса
def makeInlineKeyboard_chooseCourses(courses=[]):

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
def makeInlineKeyboard_chooseGroups(groups_list=[]):
    markup = types.InlineKeyboardMarkup()
    for group in groups_list:
        name = group['name']
        courses_id = group['group_id']
        data = json.dumps({"group_id": courses_id})
        markup.add(types.InlineKeyboardButton(text=name, callback_data=data))
    # Кнопка назад
    data = json.dumps({"group_id": "back"})
    markup.add(types.InlineKeyboardButton(text='<', callback_data=data))
    return markup


# Кнопка "Настройка уведомлений"
def makeInlineKeyboard_remining(time=0):
    markup = types.InlineKeyboardMarkup()
    data = json.dumps({"remining_btn": time})
    markup.add(types.InlineKeyboardButton(text='Настройки ⚙', callback_data=data))
    data = json.dumps({"remining_btn": "close"})
    markup.add(types.InlineKeyboardButton(text='Свернуть', callback_data=data))
    return markup


# Кнопки настройки уведомлений
def makeInlineKeyboard_custRemining(time=0):
    markup = types.InlineKeyboardMarkup()
    # data = json.dumps({"remening": time})
    actions = ['del', 'None', 'add']
    data_del = json.dumps({"remining_del": time})
    if time != 0:
        text_check = f'{time} мин'
    else:
        text_check = 'off'
    data_add = json.dumps({"remining_add": time})
    markup.add(types.InlineKeyboardButton(text='-', callback_data=data_del),
               types.InlineKeyboardButton(text=text_check, callback_data='None'),
               types.InlineKeyboardButton(text='+', callback_data=data_add))
    # Кнопка Сохранить
    data_save = json.dumps({"remining_save": time})
    markup.add(types.InlineKeyboardButton(text='Сохранить', callback_data=data_save))
    return markup
