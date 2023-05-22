import telebot
from telebot import types
import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from config import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)

data_reviews = pd.read_csv('text_for_ML.csv')
data_reviews = data_reviews.drop(columns=["id"])

nltk.download('punkt')

new_text = []
for i in data_reviews.text:
    # удаляем неалфавитные символы
    text = re.sub("[^a-zA-Zа-яА-Я]", " ", i)
    # токенизируем слова
    text = nltk.word_tokenize(text, language="russian")
    # лемматирзируем слова
    # text = [word for word in text if (word not in ru_stopwords)]
    # text = [morph.normal_forms(word) for word in text if (word not in ru_stopwords)]
    # соединяем слова
    strin = ' '.join(text)
    new_text.append(strin.strip())
    """
    strin = ""
    for i in text:
        for j in i:
            strin = strin + " " + j
    new_text.append(strin)
    """

count = CountVectorizer()
# проводим преобразование текста
matrix = count.fit_transform(new_text).toarray()
X = matrix
y = data_reviews["target"].values
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

logreg = LogisticRegression()
result_logreg = logreg.fit(x_train, y_train)
print(logreg.score(x_test, y_test))


def emotional_coloring(text):
    test_text_1 = re.sub("[^a-zA-Zа-яА-Я]", " ", text)
    test_text_2 = nltk.word_tokenize(test_text_1, language="russian")
    # test_text_3 = [word for word in test_text_2 if (word not in ru_stopwords)]
    # test_text_3 = [morph.normal_forms(word) for word in test_text_2 if (word not in ru_stopwords)]
    """
    strin_2 = ""
    for i in test_text_3:
        for j in i:
            strin_2 = strin_2 + " " + j
    """
    strin_2 = ' '.join(test_text_2)
    strin_2 = strin_2.strip()
    new_list = [strin_2]
    new = count.transform(new_list).toarray()
    result = logreg.predict(new)
    if result[0] == 0:
        return "злой текст:("
    elif result[0] == 1:
        return "добрый текст:)"


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
    result = emotional_coloring(message.text)
    if result == "злой текст:(":
        bot.send_message(message.chat.id, "Ваш текст отрицательного содержания", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Ваш текст положительного содержания", parse_mode='html')


bot.polling(none_stop=True)
