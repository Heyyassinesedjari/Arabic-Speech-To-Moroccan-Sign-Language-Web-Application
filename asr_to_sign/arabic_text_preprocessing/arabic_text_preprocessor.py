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
        

import logging
from typing import List

class ArabicTextPreprocessor:
    """
    Orchestrates a pipeline of preprocessing steps to prepare Arabic text
    for sign language translation.
    """

    def __init__(self, steps):
        self.steps = steps


    def preprocess(self, text: str) -> List[str]:
        """
        Applies all preprocessing steps in order to the input text.

        Args:
            text (str): The input Arabic text.

        Returns:
            List[str]: List of tokens ready for sign video mapping.
        """
        data = text
        for step in self.steps:
            try:
                data = step.process(data)
            except Exception as e:
                logging.error(f"Preprocessing failed at {step.__class__.__name__}: {e}")
                raise RuntimeError(f"Error in {step.__class__.__name__}: {e}")
        return data