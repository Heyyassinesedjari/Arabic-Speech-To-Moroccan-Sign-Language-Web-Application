from .interfaces import PreprocessingStep
import unicodedata
import logging

class ArabicTextNormalizerStep(PreprocessingStep):
    def __init__(self):
        pass
        
    def process(self, list_of_words: list[str]) -> list[str]:
        logging.info("Starting ArabicTextNormalizerStep")
        try:
            for i in range(len(list_of_words)):
                list_of_words[i] = unicodedata.normalize('NFKC', list_of_words[i])
            logging.info("Finished ArabicTextNormalizerStep")
            return list_of_words
        except Exception as e:
            logging.error(f"ArabicTextNormalizerStep failed: {e}")
            raise Exception(f"ArabicTextNormalizerStep failed: {e}")


