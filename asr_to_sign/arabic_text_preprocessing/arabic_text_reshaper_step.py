#TODO: Add Args and Returns examples in class method docstring.
#TODO: Add Typing, Docstring, Inline Comments
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration


from bidi import get_display
from asr_to_sign.interfaces import PreprocessingStep
import arabic_reshaper
import logging

class ArabicTextReshaperStep(PreprocessingStep):
    def __init__(self):
        pass
        
    def process(self, list_of_words: list[str]) -> list[str]:
        logging.info("Starting ArabicTextReshaperStep")
        try:
            for i in range(len(list_of_words)):
                list_of_words[i] = arabic_reshaper.reshape(list_of_words[i])
                list_of_words[i] = get_display(list_of_words[i])
            logging.info("Finished ArabicTextReshaperStep")
            return list_of_words
        except Exception as e:
            logging.error(f"ArabicTextReshaperStep failed: {e}")
            raise Exception(f"ArabicTextReshaperStep failed: {e}")