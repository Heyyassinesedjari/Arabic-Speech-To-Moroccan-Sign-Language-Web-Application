#TODO: Add Args and Returns examples in class method docstring.
#TODO: Add Typing, Docstring, Inline Comments
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration


import logging
from asr_to_sign.interfaces import PreprocessingStep
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