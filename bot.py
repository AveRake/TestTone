import telebot
from telebot import types

from config import BOT_TOKEN, VERBOSE_LOGS
from model import Model


bot = telebot.TeleBot(BOT_TOKEN)
model = Model(verbose=VERBOSE_LOGS)


@bot.message_handler(commands=['start'])
def star(message):
    mess = f'Hello, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['inf'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Find out information about me", url="https://ru.wikipedia.org/wiki/Анализ_"
                                                                               "тональности_текста"))
    bot.send_message(message.chat.id, 'I am a telegram bot that can parse text', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    result = model.emotional_coloring(message.text)
    if result == "злой текст:(":
        bot.send_message(message.chat.id, "Ваш текст отрицательного содержания", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Ваш текст положительного содержания", parse_mode='html')


bot.polling(none_stop=True)
