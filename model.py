import re
import nltk
from joblib import dump, load
import pickle

from config import PRE_TRAINED_WEIGHTS_FILENAME, PRE_TRAINED_VECTORIZER_FILENAME
from train import Trainer


class Model:
    def __init__(self, verbose=True):
        self.verbose = verbose
        if self.verbose:
            print("Initializing ML model...")

        self.trainer = Trainer()
        self.logreg = None
        self.vectorizer = None

        self.load_from_file_or_train()

    def load_from_file_or_train(self):
        try:
            self.logreg = load(PRE_TRAINED_WEIGHTS_FILENAME)
            self.vectorizer = pickle.load(open(PRE_TRAINED_VECTORIZER_FILENAME, "rb"))

            if self.verbose:
                print("Loaded pretrained model")
        except FileNotFoundError:
            if self.verbose:
                print("Training ML model...")

            self.logreg, self.vectorizer = self.trainer.get_trained_logreg()
            dump(self.logreg, PRE_TRAINED_WEIGHTS_FILENAME)
            pickle.dump(self.vectorizer, open(PRE_TRAINED_VECTORIZER_FILENAME, "wb"))

        if self.verbose:
            print("ML model is ready!")

    def emotional_coloring(self, text):
        test_text_1 = re.sub("[^a-zA-Zа-яА-Я]", " ", text)
        test_text_2 = nltk.word_tokenize(test_text_1, language="russian")

        string_2 = ' '.join(test_text_2)
        string_2 = string_2.strip()
        new_list = [string_2]
        new = self.vectorizer.transform(new_list).toarray()
        result = self.logreg.predict(new)
        if result[0] == 0:
            return "злой текст:("
        elif result[0] == 1:
            return "добрый текст:)"
