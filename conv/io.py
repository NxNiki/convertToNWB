"""Utility functions for managing files."""

import os
import pickle

import yaml

###################################################################################################
###################################################################################################

### FILE UTILITIES

def check_ext(file_name, ext):
    """Check the extension for a file name, and add if missing.

    Parameters
    ----------
    file_name : str
        The name of the file.
    ext : str
        The extension to check and add.

    Returns
    -------
    str
        File name with the extension added.
    """

    return file_name + ext if not file_name.endswith(ext) else file_name


def check_folder(file_name, folder):
    """Check a file name, adding folder path if needed.

    Parameters
    ----------
    file_name : str
        The name of the file.
    folder : str or Path, optional
        Folder location of the file.

    Returns
    -------
    str
        Full path of the file.
    """

    return os.path.join(folder, file_name) if folder else file_name


def drop_hidden_files(files):
    """Clean hidden files from a list of files."""

    return [file for file in files if file[0] != '.']


def ignore_files(files, ignore):
    """Select files based on a search term of interest."""

    return [file for file in files if ignore not in file]


def select_files(files, search):
    """Select files based on a search term of interest."""

    return [file for file in files if search in file]


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

    with open(check_ext(check_folder(file_name, folder), '.yaml'), 'r') as fobj:
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

    with open(check_ext(check_folder(file_name, folder), '.yaml'), 'w') as file:
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

    Notes
    -----
    Task objects are saved and loaded as pickle files.
    """

    with open(check_ext(check_folder(file_name, folder), '.p'), 'wb') as fobj:
        pickle.dump(task, fobj)


def load_task_object(file_name, folder=None):
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

    Notes
    -----
    Task objects are saved and loaded as pickle files.
    """

    with open(check_ext(check_folder(file_name, folder), '.p'), 'rb') as load_obj:
        task = pickle.load(load_obj)

    return task
