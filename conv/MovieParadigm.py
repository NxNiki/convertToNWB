"""
create files in .nwb format for the movie paradigm experiments
"""
import warnings
from typing import List
from settings import VALID_DEVICE
import os
import glob
import re


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
        self.micro_channels = []
        self.macro_channels = []

    @property
    def patient_id(self) -> str:

        if self.device == VALID_DEVICE['neuralynx']:
            patient_ids = [re.findall(folder, r'D\d{3}') for folder in self.input_folders]
        elif self.device == VALID_DEVICE['blackrock']:
            raise NotImplementedError("blackrock not implemented")
        else:
            raise ValueError(f"Unknown device: {self.device}. Valid values are {VALID_DEVICE}")

        unique_patient_id = list(set(patient_ids))
        if len(unique_patient_id) == 0:
            raise ValueError(f"no patient id detected in the input folders: {self.input_folders}")
        elif len(unique_patient_id) > 1:
            raise ValueError(f"multiple patient id detected in the input folders: {self.input_folders}")
        else:
            patient_id = str(unique_patient_id[0])

        return patient_id

    def parse_input_folder(self) -> List[dict]:
        """
        Extract information about patient, experiment, and channel based on directory and file names.
        confirm the patient id are same in the input folders.

        Returns:
            A list of dicts with fields patient, experiments, and channels. For each session, the dict has the following
            fields:
                subject_id
                experiment
                date
                micro
                macro
        """

        exp_info = []
        for folder in self.input_folders:
            metadata = re.match(
                r".*/(?P<subject_id>D\d+)/(?P<experiment>EXP\d+_\w+)/(?P<date>\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})/",
                folder,
            ).groupdict()

            # list micro channels:
            micro_files = glob.glob(os.path.join(folder, r'G[A-D][1-9]*.ncs'))
            macro_files = glob.glob(os.path.join(folder, r'[A-Z]+[1-9].ncs'))

            micro_channels = {os.path.basename(f) for f in micro_files}
            if not self.micro_channels:
                self.micro_channels = micro_channels
            elif self.micro_channels != micro_channels:
                warnings.warn(f"micro channels not consistent across experiments!", category=UserWarning)

            self.micro_channels |= micro_channels

            macro_channels = {os.path.basename(f) for f in macro_files}
            if not self.macro_channels:
                self.macro_channels = macro_channels
            elif self.macro_channels != macro_channels:
                warnings.warn(f"macro channels not consistent across experiments!", category=UserWarning)

            self.macro_channels |= macro_channels

            metadata['micro'] = micro_files
            metadata['macro'] = macro_files
            exp_info.append(metadata)

        self.micro_channels = sorted(list(self.micro_channels))
        self.macro_channels = sorted(list(self.macro_channels))

        return exp_info

    def create_folder(self, subject_id, experiment):
        pass



