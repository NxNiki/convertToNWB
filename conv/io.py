"""Utility functions for managing files."""

import os
import pickle

import yaml

###################################################################################################
###################################################################################################

### GENERAL FILE I/O

def get_files(folder, select=None, ignore=None, drop_hidden=True):
    """Get a list of files from a directory."""

    files = os.listdir(folder)

    # If requested, drop any hidden files (leading .'s)
    if drop_hidden:
        files = drop_hidden_files(files)

    # If requested, filter files to those that containing given search terms
    if select:
        files = select_files(files, select)

    # If requested, filter files to ignore any containing given search terms
    if ignore:
        files = ignore_files(files, ignore)

    return files


def drop_hidden_files(files):
    """Clean hidden files from a list of files."""

    return [file for file in files if file[0] != '.']


def ignore_files(files, ignore):
    """Select files based on a search term of interest."""

    return [file for file in files if ignore not in file]


def select_files(files, search):
    """Select files based on a search term of interest."""

    return [file for file in files if search in file]


#### DATA FILES

def make_file_list(files):
    """Make a list of subject files."""

    file_list = []
    for subj, sessions in files.items():
        for session in sessions:
            file_list.append(subj + '_' + session)

    return file_list

#### CONFIG FILES

def load_config(file_name, folder=None):
    """Load an individual config file."""

    file_name = os.path.join(folder, file_name) if folder else file_name
    with open(file_name, 'r') as fobj:
        data = yaml.safe_load(fobj)

    return data


def load_configs(files, folder=None):
    """Load all configs together."""

    configs = {}
    for file in files:
        label = file.split('_')[0]
        configs[label] = load_config(file, folder=folder)

    return configs


def save_config(cdict, file_name, folder=None):
    """Save out a config file."""

    file_name = os.path.join(folder, file_name) if folder else file_name
    with open(file_name + '.yaml', 'w') as file:
        yaml.dump(cdict, file)


### TASK OBJECTS

def save_task_object(task, file_name, folder=None):
    """Save a task object.

    Parameters
    ----------
    task : Task
        Task object to save out.
    file_name : str
        Name for the file to be saved out.
    folder : str or Path, optional
        Folder to save out to.
    """

    file_name = file_name + '.p' if file_name.split('.')[-1][-2:] != '.p' else file_name
    file_path = os.path.join(folder, file_name) if folder else file_name

    with open(file_path, 'wb') as file_path:
        pickle.dump(task, file_path)


def load_object(file_name, folder=None):
    """Load a task object.

    Parameters
    ----------
    file_name : str
        File name of the object to be loaded.
    folder : str or Path, optional
        Folder to load from.

    Returns
    -------
    task
        Loaded task object.
    """

    file_name = file_name + '.p' if file_name.split('.')[-1][-2:] != '.p' else file_name
    file_path = os.path.join(folder, file_name) if folder else file_name

    with open(file_path, 'rb') as load_obj:
        task = pickle.load(load_obj)

    return task
