from asr_to_sign.utils.file_existence_checker import ArabicFileExistenceChecker
import os

#TODO: Add docstring and comments where needed
#TODO: Add private methods where applicable
#TODO: Add logging where applicable and remove print statements
#TODO: Resolve any overlapping methods with file_manager.py and refactor if needed
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


class VideoRepository:
    def __init__(self, base_path="static/database/"):
        self.base_path = base_path
        self.arabic_file_existence_checker = ArabicFileExistenceChecker()

    def video_exists(self, word):
        path = os.path.join(self.base_path, f"{word}.mp4")
        return os.path.exists(path)
    
    
    def _get_video_path(self, word):
        if len(word)==1:
            if self.video_exists(word):
                print(f"{word}.mp4 exists")
                return os.path.join(self.base_path, f"{word}.mp4")
            else:
                print(f"{word}.mp4 does not exist")
                return None
        else:
            path = os.path.join(self.base_path, f"{word}.mp4")
            exists, video_file_name = self.arabic_file_existence_checker.exists(file_path=path)
            if exists:
                print(f"{word}.mp4 exists")
                new_path = os.path.join(self.base_path, video_file_name)
                return new_path
            else:
                print(f"{word}.mp4 does not exist")
                return None
            
    def get_video_paths(self, videos_names):
        videos_paths = []
        # Iterate over each video name to get its corresponding file path
        for name in videos_names:
            path = self._get_video_path(name)
            if path is not None:
                # Add the path to the list if the video exists
                videos_paths.append(path)

        # Reverse the list of paths so the concatenation order matches the input text order
        videos_paths.reverse()
        return videos_paths