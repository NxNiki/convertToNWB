"""Utility & helper functions for doing data conversion."""

import numpy as np

###################################################################################################
###################################################################################################

def clean_strings(lst):
    """Helper function to clean a list of string values for adding to NWB.

    Parameters
    ----------
    lst : list
        A list of (mostly) strings to be prepped for adding to NWB.

    Returns
    -------
    lst
        Cleaned list.

    Notes
    -----
    Each element is checked:
    - str types and made lower case and kept
    - any other type is replaced with 'none' (as a string)
    - the goal is to replace Python nan or None types for empty cells
    """

    return [val.lower() if isinstance(val, str) else 'none' for val in lst]


def get_event_time(event_times, start, end):
    """Select an event based on time range, returning NaN if not found.

    Parameters
    ----------
    events : 1d array
        Event times.
    start, end : float
        Start and end times to select between.

    Returns
    -------
    event : float or np.nan
        The selected event time, if found, or NaN.
    """

    try:
        event = event_times[np.logical_and(event_times >= start, event_times <= end)][0]
    except IndexError:
        event = np.nan

    return event
