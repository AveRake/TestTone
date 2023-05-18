import telebot
from telebot import types

bot = telebot.TeleBot('6288331035:AAHbLOrsOzsh461YLODeUg-RpG3rpgnYBBc')


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
    if message.text == "Hello" or message.text == "hello" or message.text == "hi":
        bot.send_message(message.chat.id, "Hello to you too!", parse_mode='html')
    elif message.text == "id":
        bot.send_message(message.chat.id, f"Your id is {message.from_user.id}", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Unfortunately, I am not yet able to carry out the tone of your entered text.", parse_mode='html')


bot.polling(none_stop=True)

