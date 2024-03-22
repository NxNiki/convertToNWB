"""
Utility functions for managing files.
create files in .nwb format for the movie paradigm experiments
"""
# Link in functions from convnwb - ADD ANY EXTRA FUNCTIONS NEEDED
from convnwb.io import (load_config, load_configs, save_config,
                        load_task_object, save_task_object,
                        open_h5file, save_nwbfile)
from convnwb.io.utils import get_files, make_session_name, make_file_list, missing_files
import warnings
from pathlib import Path
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
            The folders have a pattern of:
            '/<base_dir>/D<patient_id>/EXP<experiment_id>_<experiment_name>/<experiment_time>/'
            This information will be extracted as metadata.

            project_folder (str): The directory to save the converted .nwb files.

            device (str): 'neuralynx' or 'blackrock'


        Returns:
            str: A greeting message that includes the input name.
        """

        self.input_folders = input_folders
        self.project_folder = project_folder
        self.device = device
        self.patient_id = ''

        # metadata has same length as input_folders
        self.metadata = []  # List[dict]
        self.experiment_id = []  # List[int]
        self.experiment_name = []  # List[str]

        # common micro and macro channels across all experiments:
        self.micro_channels = []
        self.macro_channels = []

        self.micro_output_files = []
        self.macro_output_files = []

    def get_patient_id(self) -> str:

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
            self.patient_id = str(unique_patient_id[0])

        return self.patient_id

    def extract_metadata(self) -> List[dict]:
        """
        Extract information about patient, experiment, and channel based on directory and file names.
        confirm the patient id are same in the input folders.

        Returns:
            A list of dicts with fields patient, experiments, and channels. For each session, the dict has the following
            fields:
                subject_id
                experiment_id
                experiment_name
                date
                micro
                macro
        """

        for folder in self.input_folders:
            metadata = re.match(
                r".*/(?P<patient_id>D\d+)"
                r"/(?P<experiment_id>EXP\d+)_(?P<experiment_name>\w+)"
                r"/(?P<experiment_date>\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})/",
                folder,
            ).groupdict()

            # list micro channels:
            micro_files = glob.glob(os.path.join(folder, r'G[A-D][1-9]*.ncs'))
            macro_files = glob.glob(os.path.join(folder, r'[A-Z]+[1-9].ncs'))
            metadata['micro'] = micro_files
            metadata['macro'] = macro_files
            self.metadata.append(metadata)
            self.experiment_id.append(int(metadata["experiment_id"]))
            self.experiment_name.append(metadata["experiment_name"])

            # find common micro and macro channels across experiments:
            micro_channels = {Path(f).stem for f in micro_files}
            if not self.micro_channels:
                self.micro_channels = micro_channels
            elif self.micro_channels != micro_channels:
                warnings.warn(f"micro channels not consistent across experiments!", category=UserWarning)

            self.micro_channels |= micro_channels

            macro_channels = {Path(f).stem for f in macro_files}
            if not self.macro_channels:
                self.macro_channels = macro_channels
            elif self.macro_channels != macro_channels:
                warnings.warn(f"macro channels not consistent across experiments!", category=UserWarning)

            self.macro_channels |= macro_channels

        self.micro_channels = sorted(list(self.micro_channels))
        self.macro_channels = sorted(list(self.macro_channels))

        return self.metadata

    def create_output_path(self):
        """
        create output folder and file names (.nwb) based on metadata.

        The structure of output files:
        project_folder
            - sub-<patient_id>_exp-<experiment_id[0]>-<experiment_id[1]>...
                - micro
                    - <micro_channels[0]>.nwb
                    - <micro_channels[1]>.nwb
                    ...
                - macro
                    - <macro_channels[0]>.nwb
                    - <macro_channels[1]>.nwb
                    ...
        """

        output_folder = Path(os.path.join(
            self.project_folder,
            f"sub-{self.patient_id}_exp-{'-'.join(map(str, self.experiment_id))}"
        ))

        for channel in self.micro_channels:
            self.micro_output_files.append(output_folder.joinpath(f"micro/{channel}.nwb"))

        for channel in self.macro_channels:
            self.macro_output_files.append(output_folder.joinpath(f"macro/{channel}.nwb"))





