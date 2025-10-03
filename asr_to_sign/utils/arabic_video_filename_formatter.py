#TODO: Add Args and Returns examples in format method docstring.
#TODO: Add Typing
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration

import arabic_reshaper
import unicodedata
from bidi.algorithm import get_display
import logging


class ArabicVideoFilenameFormatter:
    """
    Utility class to format Arabic video filenames for consistent comparison.

    Primarily used in conjunction with ArabicFileExistenceChecker to normalize and format Arabic filenames
    for robust and accurate file existence checks in directories containing sign language video files named with Arabic words or letters.

    """

    def format(self, filename):
        """
        Format an Arabic video filename by normalizing Unicode representations and reshaping for proper display.
        
        Args:
            filename (str): The original Arabic filename.
                Example:

        Returns:
            str: The formatted Arabic filename.
                Example:
        
        Raises:
            Exception: If formatting fails for any reason.
        """
        try:
            logging.info(f"Formatting Arabic filename: {filename}")

            # Remove the file extension (e.g., '.mp4') to get the base filename
            filename_without_ext = filename.split('.')[0]
            arabic_word = filename_without_ext

            # Normalize Unicode representation for consistency
            arabic_word = unicodedata.normalize('NFKC', arabic_word)

            # Reshape the Arabic text for proper character joining
            reshaped_text = arabic_reshaper.reshape(arabic_word)

            # Apply right-to-left display for Arabic script
            proper_arabic = get_display(reshaped_text)
 
            # Add the '.mp4' extension back to the processed filename
            preprocessed_filename = proper_arabic + ".mp4"

            logging.info(f"Formatted Arabic filename: {preprocessed_filename}")
            return preprocessed_filename
        except Exception as e:
            logging.error(f"Failed to format Arabic filename: {e}")
            raise Exception(f"Failed to format Arabic filename: {e}")
