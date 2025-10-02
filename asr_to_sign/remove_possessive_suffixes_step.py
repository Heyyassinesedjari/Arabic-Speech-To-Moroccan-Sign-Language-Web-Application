from .interfaces import PreprocessingStep
import logging

class RemovePossessiveSuffixesStep(PreprocessingStep):
    def __init__(self, possessive_suffixes=["ي", "ه", "ك", "هم", "نا", "هن", "ها", "كن", "هن", "كما"]):
        self.possessive_suffixes = possessive_suffixes

    def process(self, list_of_words: list[str]) -> list[str]:
        # Remove possessive suffixes
        try:
            logging.info("Starting RemovePossessiveSuffixesStep")
            processed_list_of_words = []
            for word in list_of_words:
                for possessive_suffix in self.possessive_suffixes:
                    if len(word) == 1:
                        continue
                    if word.endswith(possessive_suffix):
                        word = word.replace(possessive_suffix, "")
                        break
                processed_list_of_words.append(word)
            logging.info("Finished RemovePossessiveSuffixesStep")
            return processed_list_of_words
        except Exception as e:
            logging.error(f"RemovePossessiveSuffixesStep failed: {e}")
            raise Exception(f"RemovePossessiveSuffixesStep failed: {e}")

