#TODO: Add Args and Returns examples in class method docstring.
#TODO: Add Typing, Docstring, Inline Comments
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration


from asr_to_sign.interfaces import PreprocessingStep
import re
import logging


#all process methods expect a list of words here.
class RemoveDefiniteArticleStep(PreprocessingStep):
    def process(self, list_of_words: list[str]) -> list[str]:
        logging.info("Starting RemoveDefiniteArticleStep")
        try:
            # Remove the definite article "ال" from the beginning of words using regex
            list_of_words = re.sub(r'\bال(\w+)\b', r'\1', " ".join(list_of_words)).split()
            logging.info("Finished RemoveDefiniteArticleStep")
            return list_of_words
        except Exception as e:
            logging.error(f"RemoveDefiniteArticleStep failed: {e}")
            raise Exception(f"RemoveDefiniteArticleStep failed: {e}")