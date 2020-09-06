from pprint import pprint

import telebot
import json
from time import sleep
import os

from functions.storage import MongodbService

from functions.near_lesson import get_near_lesson

from flask import Flask, request
import requests
import json

from functions.creating_buttons import makeReplyKeyboard_startMenu, makeInlineKeyboard_chooseInstitute, \
    makeInlineKeyboard_chooseCourses, makeInlineKeyboard_chooseGroups, makeInlineKeyboard_remining, \
    makeInlineKeyboard_custRemining

TOKEN = os.environ.get('TOKEN')
TIMER_URL = os.environ.get('TIMER_URL')
HOST_URL = os.environ.get('HOST_URL')

bot = telebot.TeleBot(TOKEN, threaded=False)

storage = MongodbService()  # .get_instance()

app = Flask(__name__)


@app.route(f'/{TOKEN}', methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return 'ok', 200


# ==================== Обработка команд ==================== #

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    # Проверяем есть пользователь в базе данных
    if storage.get_user(chat_id):
        storage.delete_user_or_userdata(chat_id)  # Удаляем пользвателя из базы данных

    bot.send_message(chat_id=chat_id, text='Привет!\n')
    bot.send_message(chat_id=chat_id, text='Для начала пройдите небольшую регистрацию😉\n'
                                           'Выберите институт',
                     reply_markup=makeInlineKeyboard_chooseInstitute(storage.get_institutes()))


# Команда /reg
@bot.message_handler(commands=['reg'])
def registration(message):
    chat_id = message.chat.id
    storage.delete_user_or_userdata(chat_id=chat_id)
    bot.send_message(chat_id=chat_id, text='Пройдите повторную регистрацию😉\n'
                                           'Выберите институт',
                     reply_markup=makeInlineKeyboard_chooseInstitute(storage.get_institutes()))


# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text='Список команд:\n'
                                           '/reg - повторная регистрация')


# ==================== Обработка Inline кнопок ==================== #
@bot.callback_query_handler(func=lambda call: True)
def handle_query(message):
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = message.data
    print(data)

    # После того как пользователь выбрал институт
    if 'institute' in data:
        data = json.loads(data)
        courses = storage.get_courses(data['institute'])

        institute = data['institute']

        storage.save_or_update_user(chat_id=chat_id,
                                    institute=data['institute'])  # Записываем в базу институт пользователя
        try:
            # Выводим сообщение со списком курсов
            bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=f'{institute}\nВыберите курс',
                                  reply_markup=makeInlineKeyboard_chooseCourses(courses))
        except Exception as e:
            print(f'Error: {e}')
            return

        user = storage.get_user(chat_id=chat_id)

    # После того как пользователь выбрал курс или нажал кнопку назад при выборе курса
    elif 'course' in data:
        data = json.loads(data)

        # Если нажали кнопку назад
        if data['course'] == 'back':
            storage.delete_user_or_userdata(
                chat_id=chat_id)  # Удаляем информацию об институте пользователя из базы данных
            try:
                bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                      text='Выберите институт',
                                      reply_markup=makeInlineKeyboard_chooseInstitute(storage.get_institutes()))
                return
            except Exception as e:
                print(f'Error: {e}')
                return

        groups = storage.get_groups(data['course'])

        storage.save_or_update_user(chat_id=chat_id, course=data['course'])  # Записываем в базу курс пользователя
        user = storage.get_user(chat_id=chat_id)
        institute = user['institute']
        course = user['course']
        try:
            # Выводим сообщение со списком групп
            bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                  text=f'{institute}, {course}\nВыберите группу',
                                  reply_markup=makeInlineKeyboard_chooseGroups(groups))
        except Exception as e:
            print(f'Error: {e}')
            return

    # После того как пользователь выбрал группу или нажал кнопку назад при выборе группы
    elif 'group' in data:
        data = json.loads(data)

        # Если нажали кнопку назад
        if data['group'] == 'back':
            storage.delete_user_or_userdata(chat_id=chat_id,
                                            delete_only_course=True)  # Удаляем информацию о курсе пользователя из базы данных
            institute = storage.get_user(chat_id=chat_id)['institute']
            courses = storage.get_courses(institute=institute)

            try:
                # Выводим сообщение со списком курсов
                bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=f'{institute}\nВыберите курс',
                                      reply_markup=makeInlineKeyboard_chooseCourses(courses))
                return
            except Exception as e:
                print(f'Error: {e}')
                return

        storage.save_or_update_user(chat_id=chat_id, group=data['group'])  # Записываем в базу группу пользователя

        try:
            # Удаляем меню регистрации
            bot.delete_message(message_id=message_id, chat_id=chat_id)
        except Exception as e:
            print(f'Error: {e}')
            return

        bot.send_message(chat_id=chat_id,
                         text='Вы успешно зарегистрировались!😊\n\n'
                              'Для того чтобы пройти регистрацию повторно, воспользуйтесь командой /reg',
                         reply_markup=makeReplyKeyboard_startMenu())

    elif 'remining_btn' in data:
        data = json.loads(data)
        if data['remining_btn'] == 'close':
            try:
                bot.delete_message(message_id=message_id, chat_id=chat_id)
                return
            except Exception as e:
                print(f'Error: {e}')
                return
        time = data['remining_btn']

        try:
            bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                  text='Настройка напоминаний ⚙\n\n'
                                       'Укажите за сколько минут до начала пары должно приходить сообщение',
                                  reply_markup=makeInlineKeyboard_custRemining(time))
        except Exception as e:
            print(f'Error: {e}')
            return


    elif 'remining_del' in data:
        data = json.loads(data)
        time = data['remining_del']
        if time == 0:
            return
        time -= 5

        try:
            bot.edit_message_reply_markup(message_id=message_id, chat_id=chat_id,
                                          reply_markup=makeInlineKeyboard_custRemining(time))
        except Exception as e:
            print(f'Error: {e}')
            return


    elif 'remining_add' in data:
        data = json.loads(data)
        time = data['remining_add']
        time += 5

        try:
            bot.edit_message_reply_markup(message_id=message_id, chat_id=chat_id,
                                          reply_markup=makeInlineKeyboard_custRemining(time))
        except Exception as e:
            print(f'Error: {e}')
            return

    elif 'remining_save' in data:
        data = json.loads(data)
        time = data['remining_save']

        storage.save_or_update_user(chat_id=chat_id, reminder=time)

        try:
            bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=get_remining_status(time),
                                  reply_markup=makeInlineKeyboard_remining(time))
        except Exception as e:
            print(f'Error: {e}')
            return


def get_remining_status(time):
    '''Статус напоминаний'''
    if not time or time == 0:
        remining = 'Напоминания выключены ❌\n' \
                   'Воспользуйтесь настройками, чтобы включить'
    else:
        remining = f'Напоминания включены ✅\n' \
                   f'Сообщение придёт за {time} мин до начала пары 😇'
    return remining


# ==================== Обработка текста ==================== #
@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.chat.id
    data = message.text

    user = storage.get_user(chat_id=chat_id)

    if 'Расписание' in data and user:
        group = storage.get_user(chat_id=chat_id)['group']
        print(group)
        schedule = storage.get_schedule(group=group)
        if not schedule:
            bot.send_message(chat_id=chat_id,
                             text='Расписание временно недоступно🚫😣\n'                                           'Попробуйте позже⏱')
            return
        schedule = schedule['schedule']
        bot.send_message(chat_id=chat_id, text=f'<b>Расписание {group}</b>\n{schedule}', parse_mode='HTML')

    elif 'Ближайшая пара' in data and user:
        lessons = [{'date': '5 сентября', 'time': '09:50', 'name': 'Физика', 'aud': 'К-313'},
                   {'date': '5 сентября', 'time': '11:02', 'name': 'Матан', 'aud': 'Ж-310'}]

        near_lesson = get_near_lesson(lessons)

        if not near_lesson:
            bot.send_message(chat_id=chat_id, text='Сегодня больше пар нет 😎')
            return
        bot.send_message(chat_id=chat_id, text=f'Ближайшая пара {near_lesson["name"]}\n'
                                               f'Аудитория {near_lesson["aud"]}\n'
                                               f'Начало в {near_lesson["time"]}')

    elif 'Напоминания' in data and user:
        time = user['reminder']
        if not time:
            time = 0
        bot.send_message(chat_id=chat_id, text=get_remining_status(time),
                         reply_markup=makeInlineKeyboard_remining(time))

    else:
        bot.send_message(chat_id, text='Я вас не понимаю 😞')


if __name__ == '__main__':
    bot.skip_pending = True
    bot.remove_webhook()
    print('Бот запущен локально', flush=True)
    bot.polling(none_stop=True, interval=0)
else:
    bot.set_webhook(url=f'{HOST_URL}/{TOKEN}')
