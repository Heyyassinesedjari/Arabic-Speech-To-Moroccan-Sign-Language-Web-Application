from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
import unicodedata
from .file_manager import FileManager
import arabic_reshaper
from bidi.algorithm import get_display

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



class ArabicTextPreprocessor:

    def __init__(self, video_encoder_path):
        self.file_manager = FileManager()
        self.name_dir = self.file_manager.json_load(video_encoder_path)
        
        # Preprocess name_dir for proper Arabic rendering
        for i in range(len(self.name_dir)):
            arabic_word = self.name_dir[i]
            arabic_word = unicodedata.normalize('NFKC', arabic_word)
            reshaped_text = arabic_reshaper.reshape(arabic_word)
            proper_arabic = get_display(reshaped_text)
            self.name_dir[i] = proper_arabic

        self.alphabet = "ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي ".split()
        self.arabic_stopwords = stopwords.words('arabic')
        self.arabic_punctuation = string.punctuation + '،؛؟'
        self.possessif_suffixes = ["ي", "ه", "ك", "هم", "نا", "هن", "ها", "كن", "هن", "كما"]

    def preprocess(self, text, is_name_dir=False):
        """
        Preprocess input Arabic text for MSL translation.

        - Tokenizes text
        - Removes stopwords and punctuation
        - Removes common prefixes and possessive suffixes
        - Normalizes and reshapes for proper Arabic rendering

        Args:
            text (str): Input Arabic text.
            is_name_dir (bool): If True, skips mapping to alphabet.

        Returns:
            list: List of processed words/letters for video lookup.
        """
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in self.arabic_stopwords and word not in self.arabic_punctuation]
        processed_string = re.sub(r'\bال(\w+)\b', r'\1', " ".join(filtered_words))
        text_list = processed_string.split()

        # Remove common prefixes
        for i in range(len(text_list)):
            for pref in ['ﻟﺍ', 'لا', 'ﺍﻟ', 'ال']:
                if text_list[i].endswith(pref):
                    text_list[i] = text_list[i].replace(pref, "")

        # Remove possessive suffixes
        new_list = []
        for word in text_list:
            for suff in self.possessif_suffixes:
                if len(word) == 1:
                    continue
                if word.endswith(suff):
                    word = word.replace(suff, "")
                    break
            new_list.append(word)

        # Normalize and reshape for proper Arabic rendering
        for i in range(len(new_list)):
            arabic_word = new_list[i][::-1]
            arabic_word = unicodedata.normalize('NFKC', arabic_word)
            reshaped_text = arabic_reshaper.reshape(arabic_word)
            proper_arabic = get_display(reshaped_text)
            new_list[i] = proper_arabic

        # Map to alphabet if not in name_dir
        if not is_name_dir:
            ll = []
            for word in new_list:
                if word not in self.name_dir:
                    for char in word:
                        normalized_char = unicodedata.normalize('NFKC', char)
                        ll.append(normalized_char)
                else:
                    ll.append(word)
            list_of_preprocessed_text = [string for string in ll if (string in self.alphabet) or (len(string) > 1)]
            return list_of_preprocessed_text
        else:
            list_of_preprocessed_text = [string for string in new_list if (string in self.alphabet) or (len(string) > 1)]
            return list_of_preprocessed_text
        