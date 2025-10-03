from asr_to_sign.interfaces import PreprocessingStep
from .arabic_text_normalizer_step import ArabicTextNormalizerStep
from typing import List
import logging

class WordToSignVideoMapper(PreprocessingStep):
    def __init__(self,available_sign_videos: List[str], alphabet: List[str] = "ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي ".split()):
        self.available_sign_videos = available_sign_videos
        self.alphabet = alphabet
        self.arabic_text_normalizer_step = ArabicTextNormalizerStep()

    #TODO: Optimize it.
    def process(self, list_of_words):
        logging.info("Starting WordToSignVideoMapper")
        try:
            # Map words to sign videos
            sign_video_tokens = []
            for word in list_of_words:
                if word not in self.available_sign_videos:
                    for char in word:
                        #TODO: optimize by checking if the normalized char or the original char is in available sign videos instead of doing it at thene
                        normalized_char = self.arabic_text_normalizer_step.process([char])[0]
                        sign_video_tokens.append(normalized_char)
                else:
                    sign_video_tokens.append(word)

            #TODO: instead of checking with self.alphabet, check with self.available_sign_videos
            sign_video_tokens = [string for string in sign_video_tokens if (string in self.available_sign_videos) or (len(string) > 1)]
            logging.info("Finished WordToSignVideoMapper")
            return sign_video_tokens
        except Exception as e:
            logging.error(f"WordToSignVideoMapper failed: {e}")
            raise Exception(f"WordToSignVideoMapper failed: {e}")