from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
import os
import cv2
import subprocess
import unicodedata
from .file_manager import FileManager
from .video_repository import VideoRepository
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


class ArabicTextToSignLanguageTranslator:
    """
    Translates Arabic text to Moroccan Sign Language (MSL) video sequences.
    Handles text preprocessing, video lookup, and video concatenation.
    """

    def __init__(self, video_base_path="static/database/", video_encoder_path="static/video_encoder.json"):
        """
        Initialize the translator with video database and encoder mapping.

        Args:
            video_base_path (str): Path to the video database directory.
            video_encoder_path (str): Path to the JSON file mapping words to video indices.
        """
        self.video_base_path = video_base_path
        self.file_manager = FileManager()
        self.name_dir = self.file_manager.json_load(video_encoder_path)
        # Preprocess name_dir for proper Arabic rendering
        for i in range(len(self.name_dir)):
            arabic_word = self.name_dir[i]
            arabic_word = unicodedata.normalize('NFKC', arabic_word)
            reshaped_text = arabic_reshaper.reshape(arabic_word)
            proper_arabic = get_display(reshaped_text)
            self.name_dir[i] = proper_arabic

        self.video_repository = VideoRepository(base_path=self.video_base_path)
        self.alphabet = "ا ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي ".split()
        self.arabic_stopwords = stopwords.words('arabic')
        self.arabic_punctuation = string.punctuation + '،؛؟'
        self.possessif_suffixes = ["ي", "ه", "ك", "هم", "نا", "هن", "ها", "كن", "هن", "كما"]

    def preprocess_text(self, text, is_name_dir=False):
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
            lll = [string for string in ll if (string in self.alphabet) or (len(string) > 1)]
            return lll
        else:
            lll = [string for string in new_list if (string in self.alphabet) or (len(string) > 1)]
            return lll

    def text_to_video_paths(self, text):
        """
        Convert preprocessed text to a list of video file paths.

        Args:
            text (str): Input Arabic text.

        Returns:
            list: List of video file paths corresponding to the text.
        """
        videos_names = self.preprocess_text(text, is_name_dir=False)
        videos_paths = []
        for name in videos_names:
            path = self.video_repository.get_video_path(name)
            if path is not None:
                videos_paths.append(path)
        videos_paths.reverse()
        return videos_paths

    def concat_videos(self, video_paths, output_path="static/database/concatenated_MSL_video.mp4"):
        """
        Concatenate multiple video files into a single output video.

        Args:
            video_paths (list): List of video file paths to concatenate.
            output_path (str): Path for the output concatenated video.

        Returns:
            str or None: Path to the concatenated video, or None on error.
        """
        frames = []
        try:
            for path in video_paths:
                video = cv2.VideoCapture(path)
                while True:
                    ret, frame = video.read()
                    if not ret:
                        break
                    frames.append(frame)
                video.release()
            if not frames:
                return None
            max_height = max(frame.shape[0] for frame in frames)
            max_width = max(frame.shape[1] for frame in frames)
            resized_frames = [cv2.resize(frame, (max_width, max_height)) for frame in frames]
            temp_output = 'static/database/temp_concatenated_MSL_video.mp4'
            if os.path.exists(temp_output):
                os.remove(temp_output)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_output, fourcc, 25, (max_width, max_height))
            for frame in resized_frames:
                out.write(frame)
            out.release()
            if os.path.exists(output_path):
                os.remove(output_path)
            command = f'ffmpeg -i {temp_output} -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k {output_path}'
            subprocess.call(command, shell=True)
            return output_path
        except Exception as e:
            print(f"Error occurred during video concatenation: {str(e)}")
            return None

    def text_to_video(self, text):
        """
        Convert input text to a concatenated MSL video.

        Args:
            text (str): Input Arabic text.

        Returns:
            str or None: Path to the concatenated video, or None if no videos found.
        """
        video_paths = self.text_to_video_paths(text)
        if not video_paths:
            return None
        return self.concat_videos(video_paths)