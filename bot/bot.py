from pprint import pprint

import telebot
import json
from time import sleep
import os

from functions.storage import MongodbService
from functions.near_lesson import get_near_lesson
from functions.logger import logger

from flask import Flask, request
import requests
import json

from functions.creating_buttons import make_keyboard_start_menu, make_inline_keyboard_choose_institute, \
    make_inline_keyboard_choose_courses, make_inline_keyboard_choose_groups, make_inline_keyboard_notifications, \
    make_inline_keyboard_set_notifications

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
                     reply_markup=make_inline_keyboard_choose_institute(storage.get_institutes()))


# Команда /reg
@bot.message_handler(commands=['reg'])
def registration(message):
    chat_id = message.chat.id
    storage.delete_user_or_userdata(chat_id=chat_id)
    bot.send_message(chat_id=chat_id, text='Пройдите повторную регистрацию😉\n'
                                           'Выберите институт',
                     reply_markup=make_inline_keyboard_choose_institute(storage.get_institutes()))


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

    logger.info(f'Inline button data: {data}')

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
                                  reply_markup=make_inline_keyboard_choose_courses(courses))
        except Exception as e:
            logger.exception(e)
            return


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
                                      reply_markup=make_inline_keyboard_choose_institute(storage.get_institutes()))
                return
            except Exception as e:
                logger.exception(e)
                return

        groups = storage.get_groups(data['course'])

        storage.save_or_update_user(chat_id=chat_id, course=data['course'])  # Записываем в базу курс пользователя
        user = storage.get_user(chat_id=chat_id)

        try:
            institute = user['institute']
            course = user['course']
            # Выводим сообщение со списком групп
            bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                  text=f'{institute}, {course}\nВыберите группу',
                                  reply_markup=make_inline_keyboard_choose_groups(groups))
        except Exception as e:
            logger.exception(e)
            return

    # После того как пользователь выбрал группу или нажал кнопку назад при выборе группы
    elif 'group' in data:
        data = json.loads(data)

        # Если нажали кнопку назад
        if data['group'] == 'back':
            storage.delete_user_or_userdata(chat_id=chat_id,
                                            delete_only_course=True)  # Удаляем информацию о курсе пользователя из базы данных
            try:
                institute = storage.get_user(chat_id=chat_id)['institute']
            except Exception as e:
                logger.exception(e)
                return
            courses = storage.get_courses(institute=institute)

            try:
                # Выводим сообщение со списком курсов
                bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=f'{institute}\nВыберите курс',
                                      reply_markup=make_inline_keyboard_choose_courses(courses))
                return
            except Exception as e:
                logger.exception(e)
                return

        storage.save_or_update_user(chat_id=chat_id, group=data['group'])  # Записываем в базу группу пользователя

        try:
            # Удаляем меню регистрации
            bot.delete_message(message_id=message_id, chat_id=chat_id)
        except Exception as e:
            logger.exception(e)
            return

        bot.send_message(chat_id=chat_id,
                         text='Вы успешно зарегистрировались!😊\n\n'
                              'Для того чтобы пройти регистрацию повторно, воспользуйтесь командой /reg',
                         reply_markup=make_keyboard_start_menu())

    elif 'notification_btn' in data:
        data = json.loads(data)
        if data['notification_btn'] == 'close':
            try:
                bot.delete_message(message_id=message_id, chat_id=chat_id)
                return
            except Exception as e:
                logger.exception(e)
                return
        time = data['notification_btn']

        try:
            bot.edit_message_text(message_id=message_id, chat_id=chat_id,
                                  text='Настройка напоминаний ⚙\n\n'
                                       'Укажите за сколько минут до начала пары должно приходить сообщение',
                                  reply_markup=make_inline_keyboard_set_notifications(time))
        except Exception as e:
            logger.exception(e)
            return

    elif 'del_notifications' in data:
        data = json.loads(data)
        time = data['del_notifications']
        if time == 0:
            return
        time -= 5

        try:
            bot.edit_message_reply_markup(message_id=message_id, chat_id=chat_id,
                                          reply_markup=make_inline_keyboard_set_notifications(time))
        except Exception as e:
            logger.exception(e)
            return

    elif 'add_notifications' in data:
        data = json.loads(data)
        time = data['add_notifications']
        time += 5

        try:
            bot.edit_message_reply_markup(message_id=message_id, chat_id=chat_id,
                                          reply_markup=make_inline_keyboard_set_notifications(time))
        except Exception as e:
            logger.exception(e)
            return

    elif 'save_notifications' in data:
        data = json.loads(data)
        time = data['save_notifications']

        storage.save_or_update_user(chat_id=chat_id, notifications=time)

        try:
            bot.edit_message_text(message_id=message_id, chat_id=chat_id, text=get_notifications_status(time),
                                  reply_markup=make_inline_keyboard_notifications(time))
        except Exception as e:
            logger.exception(e)
            return


def get_notifications_status(time):
    """Статус напоминаний"""
    if not time or time == 0:
        notifications_status = 'Напоминания выключены ❌\n' \
                               'Воспользуйтесь настройками, чтобы включить'
    else:
        notifications_status = f'Напоминания включены ✅\n' \
                               f'Сообщение придёт за {time} мин до начала пары 😇'
    return notifications_status


# ==================== Обработка текста ==================== #
@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.chat.id
    data = message.text

    logger.info(f'Inline button data: {data}')

    user = storage.get_user(chat_id=chat_id)

    if 'Расписание' in data and user:
        try:
            group = storage.get_user(chat_id=chat_id)['group']
        except Exception as e:
            logger.exception(e)
            return
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
        time = user['notifications']
        if not time:
            time = 0
        bot.send_message(chat_id=chat_id, text=get_notifications_status(time),
                         reply_markup=make_inline_keyboard_notifications(time))

    else:
        bot.send_message(chat_id, text='Я вас не понимаю 😞')


if __name__ == '__main__':
    bot.skip_pending = True
    bot.remove_webhook()
    logger.info('Бот запущен локально')
    bot.polling(none_stop=True, interval=0)
else:
    bot.set_webhook(url=f'{HOST_URL}/{TOKEN}')
