# from .interfaces import PreprocessingStep
# from tokenize import tokenize

# class TokenizationStep(PreprocessingStep):
#     def process(self, words):
#         # Tokenize the input text into words
#         return tokenize(words)


import logging
from .interfaces import PreprocessingStep
from nltk.tokenize import word_tokenize

class TokenizationStep(PreprocessingStep):
    def process(self, text):
        """
        Tokenizes the input text into a list of words.

        Args:
            text (str): The input text to tokenize.

        Returns:
            list[str]: List of tokenized words.

        Raises:
            RuntimeError: If tokenization fails.
        """
        logging.info("Starting TokenizationStep")
        try:
            tokens = word_tokenize(text)
            logging.info("Finished TokenizationStep")
            return tokens
        except Exception as e:
            logging.error(f"TokenizationStep failed: {e}")
            raise Exception(f"TokenizationStep failed: {e}")