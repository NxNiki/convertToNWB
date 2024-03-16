"""
create files in .nwb format for the movie paradigm experiments
"""
import glob
from typing import List
import os
import re

VALID_DEVICE = ['neuralynx', 'blackrock']


class MovieParadigm:

    def __init__(self, input_folders: List[str], project_folder, device='neuralynx'):
        """
        Basic parameters to create pipeline for the movie paradigm experiment.

        Parameters:
        input_folders (List[str]): The name of the person to greet.

        Returns:
        str: A greeting message that includes the input name.
        """
        self.input_folders = input_folders
        self.project_folder = project_folder
        self.device = device  # 'neuralynx' or 'blackrock'

    def parse_input_folder(self):
        if self.device == 'neuralynx':
            patient_folders = glob.glob(rf"{self.input_folder}/D\d{3}")
            patient_ids =

        else:
            raise ValueError(f"Unknown device: {self.device}. Valid values are {VALID_DEVICE}")

    def create_folder(self, subject_id, experiment):
        pass



