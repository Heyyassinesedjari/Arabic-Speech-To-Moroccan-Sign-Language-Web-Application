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



class ArabicTextToSignLanguageTranslator:

    def __init__(self, video_base_path="static/database/", available_sign_videos_json_path="static/available_sign_videos.json"):
        self.arabic_text_preprocessor = ArabicTextPreprocessor(available_sign_videos_json_path=available_sign_videos_json_path)
        self.sign_language_video_assembler = SignLanguageVideoAssembler(video_base_path=video_base_path)

    def text_to_video(self, text):
        videos_names = self.arabic_text_preprocessor.preprocess(text)
        video_paths = self.sign_language_video_assembler.get_video_paths(videos_names)
        if not video_paths:
            return None
        return self.sign_language_video_assembler.concatenate_videos(video_paths)