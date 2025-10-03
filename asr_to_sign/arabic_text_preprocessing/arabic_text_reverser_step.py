#TODO: Add Args and Returns examples in class method docstring.
#TODO: Add Typing, Docstring, Inline Comments
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration


from asr_to_sign.interfaces import PreprocessingStep
import logging


class ArabicTextReverserStep(PreprocessingStep):
    def process(self, list_of_words: list[str]) -> list[str]:
        logging.info("Starting ArabicTextReverserStep")
        try:
            for i in range(len(list_of_words)):
                list_of_words[i] = list_of_words[i][::-1]
            logging.info("Finished ArabicTextReverserStep")
            return list_of_words
        except Exception as e:
            logging.error(f"ArabicTextReverserStep failed: {e}")
            raise Exception(f"ArabicTextReverserStep failed: {e}")