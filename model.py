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

    def is_emotionally_positive(self, text: str) -> bool:
        text = re.sub("[^a-zA-Zа-яА-Я]", " ", text)
        tokens = nltk.word_tokenize(text, language="russian")
        token_string = ' '.join(tokens).strip()

        vectorized = self.vectorizer.transform([token_string]).toarray()
        result = self.logreg.predict(vectorized)

        return bool(result[0])
