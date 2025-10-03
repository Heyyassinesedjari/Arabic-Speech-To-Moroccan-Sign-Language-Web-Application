#TODO: Add Args and Returns examples in class method docstring.
#TODO: Add Typing
#TODO: See if there is any method overlap with video_repository.py and refactor if needed
#TODO: 
#       Security
#           No mention of environment variable management (e.g., for secrets).
#           Static files and database outputs are exposed in the project tree.
#TODO: CI/CD Configuration

import os
import json
import logging
from typing import Any, Optional


class JsonFileLoader:
    """
        Utility class for loading JSON data from a file.

        Primarily used to load the list of available sign language video names from a JSON file,
        but can be used for any general JSON file loading within the project.
    """

    def load(self, json_path: str) -> Optional[Any]:
        """
        Load and return JSON data from a file.

        Args:
            json_path (str): The path to the JSON file.

        Returns:
            Optional[Any]: The loaded JSON data, or None if the file does not exist or loading fails.
        
        Raises:
            Exception: If loading the JSON file fails for any reason.
        """
        # Check if the file exists
        if not os.path.exists(json_path):
            logging.warning(f"JSON file not found: {json_path}")
            return None

        try:
            # Load JSON data from the specified file
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logging.info(f"Successfully loaded JSON file: {json_path}")
            return data
        except Exception as e:
            logging.error(f"Failed to load JSON file '{json_path}': {e}")
            raise Exception(f"Failed to load JSON file '{json_path}': {e}")