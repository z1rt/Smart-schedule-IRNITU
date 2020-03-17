import telebot
import json

import DB

from config import TOKEN

from creating_buttons import makeReplyKeyboard_startMenu, makeInlineKeyboard_chooseInstitute, \
    makeInlineKeyboard_chooseCourses, makeInlineKeyboard_chooseGroups

bot = telebot.TeleBot(TOKEN)


# Обработка команд
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, text='Привет!\n')
    bot.send_message(chat_id, text='Для начала пройдите небольшую регистрацию😉\n'
                                   'Выберите институт',
                     reply_markup=makeInlineKeyboard_chooseInstitute(DB.get_institute()))


# Обработка Inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_query(message):
    chat_id = message.message.chat.id
    message_id = message.message.message_id
    data = message.data
    print(data)

    # После того как пользователь выбрал институт
    if 'inst_id' in data:
        data = json.loads(data)
        courses = DB.get_course(data['inst_id'])

        DB.set_user_inst(data['inst_id'])  # Записываем в базу институт пользователя

        # Выводим сообщение со списком курсов
        bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Выберите группа',
                              reply_markup=makeInlineKeyboard_chooseCourses(courses))

    # После того как пользователь выбрал курс
    elif 'course_id' in data:
        data = json.loads(data)
        groups = DB.get_group(data['course_id'])

        DB.set_user_course(chat_id=chat_id, course_id=data['course_id'])  # Записываем в базу курс пользователя

        # Выводим сообщение со списком групп
        bot.edit_message_text(message_id=message_id, chat_id=chat_id, text='Выберите курс',
                              reply_markup=makeInlineKeyboard_chooseGroups(groups))

    # После того как пользователь выбрал группу
    elif 'group_id' in data:
        data = json.loads(data)
        DB.set_user_group(chat_id=chat_id, group_id=data['group_id'])  # Записываем в базу группу пользователя

        # Удаляем меню регистрации
        bot.delete_message(message_id=message_id, chat_id=chat_id)

        bot.send_message(chat_id=chat_id,
                         text='Вы успешно зарегистрировалась!😊\n\n'
                              'Для того чтобы пройти регистрацию повторно, воспользуйтесь командой /reg',
                         reply_markup=makeReplyKeyboard_startMenu())


# Обработка текста
@bot.message_handler(content_types=['text'])
def text(message):
    chat_id = message.chat.id
    data = message.text

    if 'Расписание' in data:
        pass
    elif 'Ближайшая пара' in data:
        pass
    elif 'Настройка уведомлений' in data:
        pass
    else:
        bot.send_message(chat_id, text='Я вас не понимаю 😞')


if __name__ == '__main__':
    bot.skip_pending = True
    print('Бот запущен')
    bot.polling(none_stop=True, interval=0)
