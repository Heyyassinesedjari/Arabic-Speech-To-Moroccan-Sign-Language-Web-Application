import os
import cv2
import subprocess

#TODO: Security:
#If any part of the ffmpeg command comes from user input, sanitize it to avoid shell injection risks.
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
#Logging:
# Replace print with logging.error or logging.exception for error reporting.
# Error Handling:
# Consider raising more specific exceptions or returning error codes/messages.
# Docstrings:
# Add class and method docstrings for clarity.


class SignLanguageVideoAssembler:

    def assemble(self, video_paths, output_path="static/database/concatenated_MSL_video.mp4"):
        try:

            frames = self._extract_frames(video_paths)
            resized_frames, max_height, max_width = self._resize_frames(frames)
            temp_output = 'static/database/temp_concatenated_MSL_video.mp4'
            self._write_temp_video(resized_frames, max_height, max_width, temp_output)
            output_path = self._write_final_encoded_video(temp_output, output_path)
            # Return the path to the final concatenated video
            return output_path
        except Exception as e:
            print(f"Error occurred during video concatenation: {str(e)}")
            raise Exception(f"Error occurred during video concatenation: {str(e)}")
        

    def _extract_frames(self, video_paths):
        frames = []
        for path in video_paths:
            # Open each video file for reading frames
            video = cv2.VideoCapture(path)
            while True:
                # Read each frame from the video
                ret, frame = video.read()
                if not ret:
                    # Break when there are no more frames
                    break
                frames.append(frame)
            # Release the video file
            video.release()
        return frames
    
    def _resize_frames(self, frames):
        # If no frames were read from any video, return None
        if not frames:
            return None
        
        # Determine the maximum height and width among all frames
        max_height = max(frame.shape[0] for frame in frames)
        max_width = max(frame.shape[1] for frame in frames)

        # Resize all frames to the maximum dimensions for consistency
        resized_frames = [cv2.resize(frame, (max_width, max_height)) for frame in frames]
        return resized_frames, max_height, max_width

    def _write_temp_video(self, frames, max_height, max_width, temp_output='static/database/temp_concatenated_MSL_video.mp4'):
        # Remove temporary output file for concatenated video if it already exists
        if os.path.exists(temp_output):
            os.remove(temp_output)
        
        # Set up the video writer with the correct codec and dimensions
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output, fourcc, 25, (max_width, max_height))

        # Write each resized frame to the output video
        for frame in frames:
            out.write(frame)
        
        # Finalize the video file
        out.release()

    def _write_final_encoded_video(self, temp_output, output_path):
        # Remove the final output file if it already exists
        if os.path.exists(output_path):
            os.remove(output_path)
        
        # Use ffmpeg to re-encode the video for better compatibility and compression
        command = f'ffmpeg -i {temp_output} -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k {output_path}'
        subprocess.call(command, shell=True)

        # Return the path to the final concatenated video
        return output_path