import os
from flask import request
from pydub import AudioSegment
import logging

class FileManager:
    def __init__(self, base_path="static/"):
        self.base_path = base_path

    def file_exists(self, file_path):
        """Check if a file exists."""
        return os.path.exists(file_path)

    def get_file_path(self, directory):
        """Return the full path to the only file in a directory, or None if not exactly one file."""
        files = os.listdir(directory)
        if len(files) == 1:
            return os.path.join(directory, files[0])
        else:
            print(f"Directory {directory} does not contain a single file.")
            return None

    def delete_file(self, file_path):
        """Delete a file if it exists."""
        if self.file_exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
            return True
        else:
            print(f"File not found: {file_path}")
            return False
    
    def json_load(self, json_path):
        """Load and return JSON data from a file."""
        import json
        if self.file_exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"JSON file not found: {json_path}")
            return None
    

    def save_audio_file_sent_by_browser(self, output_path='static/audio.mp3'):
        """
        Save an audio file uploaded via a Flask request to the specified output path.

        Args:
            output_path (str): The path where the audio file will be saved.

        Returns:
            bool: True if the audio was saved successfully, False otherwise.
        """
        try:
            audio_file_storage = request.files['audio']
            audio_segment = AudioSegment.from_file(audio_file_storage)
            audio_segment.export(output_path, format='mp3')
            logging.info(f"Audio saved as {output_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to save audio: {e}")
            return False

    # Add more methods as needed (e.g., save_file, validate_file, etc.)