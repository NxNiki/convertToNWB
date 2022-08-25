"""Functions for processing task data."""

import numpy as np

from convnwb.timestamps.align import fit_sync_alignment, predict_times
from convnwb.utils.convert import convert_to_array, convert_type
from convnwb.utils.log import print_status

# Import local code
# from conv.measures import ...

###################################################################################################
###################################################################################################

def process_task(task, verbose=True):
    """Process task information.

    Parameters
    ----------
    task : Task
        Task object with information parsed from the logfile.

    Returns
    -------
    task : Task
        Task object with pre-processing applied.
    """

    print_status(verbose, 'processing task data:', 1)

    # Process each aspect of the task information
    task = process_time_info(task, verbose=verbose)
    task = process_trial_info(task, verbose=verbose)
    task = process_stimulus_info(task, verbose=verbose)
    task = process_position_info(task, verbose=verbose)
    task = process_error_info(task, verbose=verbose)

    # Run sync pulse time alignment
    if verbose:
        print('\trunning time alignment::')
    task = sync_fit_alignment(task, verbose=verbose)
    task = sync_apply_alignment(task, verbose=verbose)

    # Check and fix any trial number discrepancies
    if verbose:
        print('\tchecking task info:')
    task = check_task_info(task, verbose=verbose)

    return task


def process_time_info(task):
    """Process time related information."""

    print_status(verbose, 'timestamps...', 2)

    ...

    # Convert all time fields to be float values
    task.update_time(convert_to_array, skip='session', dtype=float)
    task.convert_type('session', ['start_time', 'end_time'], float)

    return task


def process_trial_info(task):
    """Process per trial task related information."""

    print_status(verbose, 'trial info...', 2)

    ...

    return task


def process_stimulus_info(task):
    """Process stimulus related information."""

    print_status(verbose, 'stimulus info...', 2)

    ...

    return task


def process_position_info(task):
    """Process continuously sampled position related information."""

    print_status(verbose, 'position info...', 2)

    ...

    return task


def process_error_info(task):
    """Process per trial error related information."""

    print_status(verbose, 'error info...', 2)

    ...

    return task


def sync_fit_alignment(task, verbose=True):
    """Process synchronization pulses."""

    print_status(verbose, 'fitting sync model...', 2)

    # Compute the sync offset time by fitting a model between time recordings
    intercept, coef, score = fit_sync_alignment(sync_behav, sync_neuro)
    task.sync['alignment']['intercept'] = intercept
    task.sync['alignment']['coef'] = coef
    task.sync['alignment']['score'] = score

    if verbose:
        print("\t\t\tcorrelation: {}".format(score))


def sync_apply_alignment(task, verbose=True):
    """Apply temporal alignment to all behavioral time stamps."""

    print_status(verbose, 'applying alignment...', 2)

    task.update_time(predict_times, skip='sync',
                     intercept=task.sync['alignment']['intercept'],
                     coef=task.sync['alignment']['coef'])

    # Might need to do something custom for sync pulses

    task.set_status('time_aligned', True)

    return task


def check_task_info(task, verbose=True):
    """Check task object for consistency."""

    print_status(verbose, 'checking task info...', 2)

    ...

    return task
