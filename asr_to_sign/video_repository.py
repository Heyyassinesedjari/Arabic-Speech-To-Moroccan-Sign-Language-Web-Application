from .file_manager import FileManager
import os
import arabic_reshaper
import unicodedata
from bidi.algorithm import get_display

class VideoRepository:
    def __init__(self, base_path="static/database/"):
        self.base_path = base_path
        self.file_manager = FileManager()

    def video_exists(self, word):
        path = os.path.join(self.base_path, f"{word}.mp4")
        return self.file_manager.file_exists(path)
    
    #TODO: get to find arabicwords.mp4 videos or encode them with alatin or numbers to retrieve them easily as arabic words are hard to handle
    def get_video_path(self, word):
        if len(word)==1:
            if self.video_exists(word):
                print(f"{word}.mp4 exists")
                return os.path.join(self.base_path, f"{word}.mp4")
            else:
                print(f"{word}.mp4 does not exist")
                return None
        else:
            path = os.path.join(self.base_path, f"{word}.mp4")
            exists, video_file_name = self.file_manager.arabic_file_exists(file_path=path)
            if exists:
                print(f"{word}.mp4 exists")
                new_path = os.path.join(self.base_path, video_file_name)
                return new_path
            else:
                print(f"{word}.mp4 does not exist")
                return None