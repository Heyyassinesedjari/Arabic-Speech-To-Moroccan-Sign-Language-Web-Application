import os
import cv2
import subprocess
from .video_repository import VideoRepository

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


class SignLanguageVideoAssembler:

    def __init__(self, video_base_path):
        self.video_base_path = video_base_path
        self.video_repository = VideoRepository(base_path=self.video_base_path)

    
    def get_video_paths(self, videos_names):
        videos_paths = []
        for name in videos_names:
            path = self.video_repository.get_video_path(name)
            if path is not None:
                videos_paths.append(path)
        videos_paths.reverse()
        return videos_paths
    

    def concatenate_videos(self, video_paths, output_path="static/database/concatenated_MSL_video.mp4"):
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
        