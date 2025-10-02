from abc import ABC, abstractmethod


class PreprocessingStep(ABC):
    @abstractmethod
    def process(self, words):
        """
        Process input (usually a list of words).
        TokenizationStep expects a string as input.
        All other steps expect a list of words.
        """
        pass