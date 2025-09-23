from .file_manager import FileManager
import os

class VideoRepository:
    def __init__(self, base_path="static/database/"):
        self.base_path = base_path
        self.file_manager = FileManager()

    def video_exists(self, word):
        path = os.path.join(self.base_path, f"{word}.mp4")
        return self.file_manager.file_exists(path)
    
    def get_video_path(self, word):
        if self.video_exists(word):
            return os.path.join(self.base_path, f"{word}.mp4")
        else:
            return None