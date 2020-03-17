import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


# Обработка команд
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id

    bot.send_message(chat_id, text='Привет!')


# Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_query(message):
    pass


# Обработка текста
@bot.message_handler(content_types=['text'])
def text(message):
    pass


if __name__ == '__main__':
    bot.skip_pending = True
    print('Бот запущен')
    bot.polling(none_stop=True, interval=0)
