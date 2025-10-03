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

class RemovePrefixesStep(PreprocessingStep):
    def __init__(self, prefixes=['ﻟﺍ', 'لا', 'ﺍﻟ', 'ال']):
        self.prefixes = prefixes

    def process(self, list_of_words: list[str]) -> list[str]:
        """
        Remove common Arabic prefixes from each word in the list.
        """
        # Remove common prefixes
        logging.info("Starting RemovePrefixesStep")
        try:
            for i in range(len(list_of_words)):
                for pref in self.prefixes:
                    # arabic rendering is weird that's why we use endswith for prefixes
                    if list_of_words[i].endswith(pref):
                        list_of_words[i] = list_of_words[i].replace(pref, "")
            logging.info("Finished RemovePrefixesStep")
            return list_of_words
        except Exception as e:
            logging.error(f"RemovePrefixesStep failed: {e}")
            raise Exception(f"RemovePrefixesStep failed: {e}")

