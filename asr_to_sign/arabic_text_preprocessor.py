#TODO: Add private methods where applicable
#TODO: Add logging where applicable
#TODO: Critique all OOP classes following SOLID principles
#TODO: Simplify as much as you can the logic of all methods in whole project
#TODO: Naming and Readability: Variable and function names may not be descriptive enough for maintainability.
#TODO: Add docstring and comments explaining non-trivial logic
#TODO: Error handling is likely minimal or ad hoc, especially in scripts and routes.
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration
        

import logging
from typing import List
from .tokenization_step import TokenizationStep
from .remove_stopwords_step import RemoveStopwordsStep
from .remove_punctuation_step import RemovePunctuationStep
from .remove_definite_article_step import RemoveDefiniteArticleStep
from .remove_prefixes_step import RemovePrefixesStep
from .remove_possessive_suffixes_step import RemovePossessiveSuffixesStep
from .arabic_text_reverser_step import ArabicTextReverserStep
from .arabic_text_normalizer_step import ArabicTextNormalizerStep
from .arabic_text_reshaper_step import ArabicTextReshaperStep
from .word_to_sign_video_mapper import WordToSignVideoMapper
from .file_manager import FileManager

class ArabicTextPreprocessor:
    """
    Orchestrates a pipeline of preprocessing steps to prepare Arabic text
    for sign language translation.
    """

    def __init__(self, available_sign_videos_json_path):

        self.available_sign_videos = FileManager().json_load(json_path=available_sign_videos_json_path)
        
        # Initialize each step (you can pass config as needed)
        self.steps = [
            TokenizationStep(),
            RemoveStopwordsStep(),
            RemovePunctuationStep(),
            RemoveDefiniteArticleStep(),
            RemovePrefixesStep(),
            RemovePossessiveSuffixesStep(),
            ArabicTextReverserStep(),
            ArabicTextNormalizerStep(),
            ArabicTextReshaperStep(),
            WordToSignVideoMapper(available_sign_videos=self.available_sign_videos)
        ]

    def preprocess(self, text: str) -> List[str]:
        """
        Applies all preprocessing steps in order to the input text.

        Args:
            text (str): The input Arabic text.

        Returns:
            List[str]: List of tokens ready for sign video mapping.
        """
        data = text
        for step in self.steps:
            try:
                data = step.process(data)
            except Exception as e:
                logging.error(f"Preprocessing failed at {step.__class__.__name__}: {e}")
                raise RuntimeError(f"Error in {step.__class__.__name__}: {e}")
        return data