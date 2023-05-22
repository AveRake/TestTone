import telebot
from telebot import types

from config import BOT_TOKEN, VERBOSE_LOGS
from model import Model


bot = telebot.TeleBot(BOT_TOKEN)
model = Model(verbose=VERBOSE_LOGS)


def get_user_name(message) -> str:
    if message.from_user.first_name is not None:
        username = ""
        username += message.from_user.first_name

        if message.from_user.last_name is not None:
            username += f" {message.from_user.last_name}"

        return username

    return message.from_user.username


@bot.message_handler(commands=['start'])
def start(message):
    response = f"""
Привет, <b>{get_user_name(message)}</b>!
Я могу определить тональность текста. Напиши мне сообщение, а я определю положительно оно окрашено или нет
"""

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "Узнать больше про анализ тональности текста",
        url="https://ru.wikipedia.org/wiki/Анализ_тональности_текста")
    )

    bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if model.is_emotionally_positive(message.text):
        bot.send_message(message.chat.id, "Ваш текст <b>положительного</b> содержания", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Ваш текст <b>отрицательного</b> содержания", parse_mode='html')


bot.polling(none_stop=True)
