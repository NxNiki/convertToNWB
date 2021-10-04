"""Functions for processing task data."""

import numpy as np

from spiketools.spatial.position import compute_speed

# Import local code
from conv.measures import compute_linear_position, compute_error
from conv.timestamps import align_times

###################################################################################################
###################################################################################################

def process_task_all(task):
    """Process all aspects of the task information.

    Parameters
    ----------
    task : Task
        Unprocessed task information.

    Returns
    -------
    task : Task
        Processed task information.
    """

    # Process each aspect of the task information
    task = process_time_info(task)
    task = process_task_info(task)
    task = process_position_info(task)
    task = process_location_info(task)
    task = process_error_info(task)

    return task


def process_time_info(task):
    """Process time related information."""

    # ....
    task['time'] = ...

    # Compute the spikeoffset time by fitting a model between time recordings
    task['spikeoffset'] = align_times(nsp_time, behavioral_time, logtimes)

    return task


def process_task_info(task):
    """Process per trial task related information."""

    ...

    return task


def process_position_info(task):
    """Process continuously sampled position related information."""

    ...

    return task


def process_location_info(task):
    """Process per trial location related information."""

    ...

    return task


def process_error_info(task, ...):
    """Process per trial error related information."""

    ...

    return task
