#TODO: Add Args and Returns examples in class method docstring.
#TODO: Add Typing, Docstring, Inline Comments
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration


from asr_to_sign.interfaces import PreprocessingStep
from string import punctuation
import logging

class RemovePunctuationStep(PreprocessingStep):
    def __init__(self, punctuation=punctuation):
        self.arabic_punctuation = punctuation + '،؛؟'

    def process(self, list_of_words: list[str]) -> list[str]:
        logging.info("Starting RemovePunctuationStep")
        try:
            list_of_words = [word for word in list_of_words if word not in self.arabic_punctuation]
            logging.info("Finished RemovePunctuationStep")
            return list_of_words
        except Exception as e:
            logging.error(f"RemovePunctuationStep failed: {e}")
            raise Exception(f"RemovePunctuationStep failed: {e}")