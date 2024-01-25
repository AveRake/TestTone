import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from config import DATASET_FILENAME


nltk.download('punkt')

class Trainer:
    def __init__(self, verbose=True):
        self.verbose = verbose

        self.data_reviews = None
        self.prepared_data = []
        self.y_test = None
        self.y_train = None
        self.x_test = None
        self.x_train = None

        self.logreg = None
        self.vectorizer = None

    def load_dataset(self):
        if self.verbose:
            print(f"Loading dataset from {DATASET_FILENAME}")

        self.data_reviews = pd.read_csv(DATASET_FILENAME)
        self.data_reviews = self.data_reviews.drop(columns=["id"])

    def prepare_data(self):
        if self.verbose:
            print("Preparing data...")

        for i in self.data_reviews.text:
            text = re.sub("[^a-zA-Zа-яА-Я]", " ", i)  # удаляем неалфавитные символы
            tokens = nltk.word_tokenize(text, language="russian")  # токенизируем слова
            token_string = ' '.join(tokens).strip()  # соединяем слова

            self.prepared_data.append(token_string)

    def train_test_split(self):
        if self.verbose:
            print("Splitting dataset to train / test...")

        self.vectorizer = CountVectorizer()

        matrix = self.vectorizer.fit_transform(self.prepared_data).toarray()  # проводим преобразование текста
        x = matrix
        y = self.data_reviews["target"].values
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.20, random_state=42)

    def train(self):
        if self.verbose:
            print("Training...")

        logreg = LogisticRegression(solver='liblinear', max_iter=1000)
        logreg = logreg.fit(self.x_train, self.y_train)

        if self.verbose:
            print(f"Trained model score: {logreg.score(self.x_test, self.y_test)}")

        return logreg

    def get_trained_logreg(self):
        self.load_dataset()
        self.prepare_data()
        self.train_test_split()
        return self.train(), self.vectorizer
