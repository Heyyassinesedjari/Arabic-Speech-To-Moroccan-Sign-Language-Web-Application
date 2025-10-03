#TODO: Add Args and Returns examples in class method docstring.
#TODO: Add Typing
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration

from flask import request
from pydub import AudioSegment
import logging


class AudioFileSaver:
    """
    Handles the saving of audio files uploaded via a Flask request.

    Primarily used to save audio input from users for further processing in the ASR to Sign Language pipeline.
    """
    def __init__(self):
        pass

    def save(self, output_path='static/audio.mp3'):
        """
        Save an audio file uploaded via a Flask request to the specified output path.

        Args:
            output_path (str): The path where the audio file will be saved.

        Returns:
            bool: True if the audio was saved successfully, False otherwise.

        Raises:
            RuntimeError: If saving the audio file fails.
        """
        try:
            logging.info("Saving audio file...")

            # Retrieve the uploaded audio file from the Flask request
            audio_file_storage = request.files['audio']
            
            # Load the audio file into a pydub AudioSegment object
            audio_segment = AudioSegment.from_file(audio_file_storage)

            # Export the audio segment as an MP3 file to the specified output path
            audio_segment.export(output_path, format='mp3')
            logging.info(f"Audio saved as {output_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to save audio: {e}")
            raise RuntimeError(f"Failed to save audio: {e}")