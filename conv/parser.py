"""Functions for parsing log files."""

import pandas as pd

# Import local code
from conv.task import Task
from conv.process import (process_time_info, process_task_info, process_position_info,
                          process_location_info, process_error_info)

###################################################################################################
###################################################################################################

def process_logfile(file_path, process=False):
    """Collect and process the task information.

    Parameters
    ----------
    file_path : str or Path
        Path to the logfile.
    process : bool, optional, default: False
        Whether to process the collected task information.
    """

    # Parse the log file
    task = parse_lines_logfile(file_path)

    if process:
        task = process_task_all(task)

    return task


def parse_lines_logfile(file_path, task=None):
    """Parse the lines of a task log file, collecting information into a Task object.

    Parameters
    ----------
    file_path : str or Path
        The path to the log file to parse information from.
    """

    # Initialize task object, if not given, for collecting data
    if not Task:
        task = Task()

    # Define flags, with start values, for tracking current status
    flags = {'task_phase': {...},
             }

    # Running counters of task information
    trial_counter = 0

    # Loop across all lines in log file and collect information
    with open(file_path, 'r') as fobj:
        for ix, line in enumerate(fobj.readlines()):

            ## Setup
            line = line.replace('\r', '')
            tokens = line[:-1].split('\t')

            # Check and collect information for different task phases
            if len(tokens) <= 3:
                print('Unexpected line length at line {}'.format(ix))
                continue

            if len(tokens) == None:
                ...

            if len(tokens) > None:
                ...


    return task


def parse_lines_sync(file_path, task=None):
    """"Parse timestamp information from a synchronization file."""

    # Initialize task object, if not given, for collecting data
    if not Task:
        task = Task()


    with open(file_path, 'r') as fobj:
        for ix, line in enumerate(fobj.readlines()):

            line = line.replace('\r', '')
            tokens = line[:-1].split('\t')

            # This is one possibility of what it looks like: EEGlog file
            task.sync_behavioral['time'].append(tokens[0])
            task.sync_behavioral['frame'].append(tokens[1])
            task.sync_behavioral['on_off'].append(tokens[2])

    return task
