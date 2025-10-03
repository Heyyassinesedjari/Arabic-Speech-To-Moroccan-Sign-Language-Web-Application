#TODO: Add Args and Returns examples in class method docstring.
#TODO: Add Typings
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration

import os
import logging


class ArabicFileExistenceChecker:
    """
    Utility class for checking the existence of files with Arabic names, specifically for sign language video lookup.

        - Sign language video files are named using Arabic words or letters, which can have multiple valid Unicode representations.
        - This class uses normalization to ensure robust and accurate file existence checks in directories containing such files (e.g. static/database/).
   
   """
    def __init__(self, filename_formatter=None):
        """
        Initialize the ArabicFileExistenceChecker.

        Args:
            filename_formatter (Optional[ArabicVideoFilenameFormatter]): 
                An object used to normalize and format filenames for accurate comparison.
                If None, a default ArabicVideoFilenameFormatter will be instantiated and used.

        Example:
            # Uses default formatter
            checker = ArabicFileExistenceChecker()
            # or
            # Uses custom formatter
            custom_formatter = ArabicVideoFilenameFormatter()
            checker = ArabicFileExistenceChecker(filename_formatter=custom_formatter)
        """
        # use default formatter if none provided
        if filename_formatter is None:
            from .arabic_video_filename_formatter import ArabicVideoFilenameFormatter
            filename_formatter = ArabicVideoFilenameFormatter()
        
        # use custom formatter if provided
        self.filename_formatter = filename_formatter

    def exists(self, file_path):
        """
        Check if a file with an Arabic name exists in the specified directory, using the provided formatter
        (e.g. ArabicVideoFilenameFormatter from utils.arabic_video_filename_formatter.py) to normalize and format filenames for robust and accurate comparison.

        Args:
            file_path (str): The full path to the target file.

        Returns:
            Tuple[bool, Optional[str]]: (True, actual filename) if found, (False, None) otherwise.
        
        Raises:
            Exception: If an error occurs during the file existence check.
        
        """
        try:
            logging.info(f"Checking existence for file: {file_path}")

            # Split the provided path into directory and filename
            directory, filename = os.path.split(file_path)
            norm_filename = filename
            
            # Iterate over all files in the target directory (e.g. static/database/)
            for f in os.listdir(directory):
                # Format each filename for robust comparison (handles Arabic normalization)
                if self.filename_formatter.format(f) == norm_filename:
                    logging.info(f"Arabic file found: {f}")
                    return True, f
            
            logging.info(f"No Arabic file found matching: {norm_filename}")
            return False, None
        
        except Exception as e:
            logging.error(f"Error while checking arabic file existence: {e}")
            raise Exception(f"Error while checking arabic file existence: {e}")
