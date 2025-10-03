from .arabic_text_preprocessing.arabic_text_preprocessor import ArabicTextPreprocessor
from .video_processing.sign_language_video_assembler import SignLanguageVideoAssembler


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

from .arabic_text_preprocessing.tokenization_step import TokenizationStep
from .arabic_text_preprocessing.remove_stopwords_step import RemoveStopwordsStep
from .arabic_text_preprocessing.remove_punctuation_step import RemovePunctuationStep
from .arabic_text_preprocessing.remove_definite_article_step import RemoveDefiniteArticleStep
from .arabic_text_preprocessing.remove_prefixes_step import RemovePrefixesStep
from .arabic_text_preprocessing.remove_possessive_suffixes_step import RemovePossessiveSuffixesStep
from .arabic_text_preprocessing.arabic_text_reverser_step import ArabicTextReverserStep
from .arabic_text_preprocessing.arabic_text_normalizer_step import ArabicTextNormalizerStep
from .arabic_text_preprocessing.arabic_text_reshaper_step import ArabicTextReshaperStep
from .arabic_text_preprocessing.word_to_sign_video_mapper import WordToSignVideoMapper
from .utils.json_file_loader import JsonFileLoader

class ArabicTextToSignLanguageTranslator:

    def __init__(self, video_base_path="static/database/", available_sign_videos_json_path="static/available_sign_videos.json" ):
        self.sign_language_video_assembler = SignLanguageVideoAssembler(video_base_path=video_base_path)
        self.available_sign_videos = JsonFileLoader().load(json_path=available_sign_videos_json_path)
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
        self.arabic_text_preprocessor = ArabicTextPreprocessor(steps=self.steps)

    def text_to_video(self, text):
        videos_names = self.arabic_text_preprocessor.preprocess(text)
        video_paths = self.sign_language_video_assembler.get_video_paths(videos_names)
        if not video_paths:
            return None
        return self.sign_language_video_assembler.concatenate_videos(video_paths)