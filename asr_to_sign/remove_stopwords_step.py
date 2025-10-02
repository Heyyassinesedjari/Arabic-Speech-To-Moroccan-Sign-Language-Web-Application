from .interfaces import PreprocessingStep
from nltk.corpus import stopwords
import logging

class RemoveStopwordsStep(PreprocessingStep):
    def __init__(self, stopwords=stopwords.words('arabic')):
        self.arabic_stopwords = set(stopwords)

    def process(self, list_of_words: list[str]) -> list[str]:
        logging.info("Starting RemoveStopwordsStep")
        try:
            list_of_words = [word for word in list_of_words if word not in self.arabic_stopwords]
            logging.info("Finished RemoveStopwordsStep")
            return list_of_words
        except Exception as e:
            logging.error(f"RemoveStopwordsStep failed: {e}")
            raise Exception(f"RemoveStopwordsStep failed: {e}")