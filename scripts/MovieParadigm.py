"""
create files in .nwb format for the movie paradigm experiments
"""
from typing import List
import os
import re

VALID_DEVICE = {
    'neurolynx': 'neuralynx',
    'blackrock': 'blackrock'
}


class MovieParadigm:

    def __init__(self, input_folders: List[str], project_folder: str, device: str ='neuralynx') -> None:
        """
        Basic parameters to create pipeline for the movie paradigm experiment.

        Parameters:
            input_folders (List[str]): The folders of movie paradigm experiments. This should be for a single patient.

            project_folder (str): The directory to save the converted .nwb files.

            device (str): 'neuralynx' or 'blackrock'


        Returns:
            str: A greeting message that includes the input name.
        """

        self.input_folders = input_folders
        self.project_folder = project_folder
        self.device = device

    @property
    def patient_id(self) -> str:
        if self.device == VALID_DEVICE['neuralynx']:
            patient_ids = [re.findall(folder, r'D\d{3}') for folder in self.input_folders]
        elif self.device == VALID_DEVICE['blackrock']:
            raise NotImplementedError("blackrock not implemented")
        else:
            raise ValueError(f"Unknown device: {self.device}. Valid values are {VALID_DEVICE}")

        patient_id = list(set(patient_ids))
        if len(patient_ids) == 0:
            raise ValueError(f"")
        return patient_id

    def parse_input_folder(self) -> List[dict]:
        """
        Extract information about patient, experiment, and channel based on directory and file names.
        confirm the patient id are same in the input folders.

        Returns:
            A list of dicts with fields patient, experiments, and channels. For each
        """

        exp_info = []
        for d in self.input_folders:




        return exp_info

    def create_folder(self, subject_id, experiment):
        pass



