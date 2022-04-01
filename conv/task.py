"""Task class."""

from copy import deepcopy

from convnwb.plts import plot_alignment

###################################################################################################
###################################################################################################

class Task(object):
    """Object for collecting task data."""

    def __init__(self):
        """Initialize task object."""

        # Set some information for tracking the task object
        self.time_reset = False
        self.time_offset = None

        # METADATA - subject / session information
        self.meta = {
            'task' : None,
            'subject' : None,
            'session' : None
        }

        # SESSION INFORMATION
        self.session = {
            'start' : None,
            'end' : None
        }

        ## SYNCHRONIZATION

        self.sync = {...}

        ## TASK STRUCTURE

        # Marker variables for particular parts of the task
        self.phase_times = {...
        }

        ## TRIALS

        # Information on task elements (navigation / encoding / recall, etc)
        self.trial = {...}
        ...

        ## POSITION

        self.pos = {'x' : [], 'y' : [], 'z' : []}

        ## BEHAVIOUR

        self.button = {'time' : [], 'x' : [], 'y' : [], 'z' : []}

        ## STIMULI

        self.stim_info = {...}


    def get_trial(self, index, field='trial'):
        """Get the information for a specified trial.

        Parameters
        ----------
        index : int
            The index of the trial to access.
        field : {'trial', ...}
            Which trial data to access.
        """

        trial_info = dict()
        for key in getattr(self, field).keys():
            trial_info[key] = getattr(self, field)[key][index]

        return trial_info


    def plot_sync_allignment(self, n_pulses=100):
        """Plots alignment of the synchronization pulses.

        Parameters
        ----------
        n_pulses : int, optional, default: 100
            Number of pulses to plot for zoomed plot.
        """

        plot_alignment(self.sync_neural['time_on'],
                       self.sync_behavioral['time_on_aligned'],
                       n_pulses=n_pulses)


def offset_task_time(task, offset):
    """Offset all timestamps within a task object.

    Parameters
    ----------
    task : Task
        Task object.
    offset : float
        The time value to subtract from each logged time value.

    Returns
    -------
    task : Task
        Updated task object.

    Notes
    -----
    This function returns a copy of the task object, so it won't overwrite in place.
    """

    task = deepcopy(task)

    # Session - session start & end times
    for attr in ['start', 'end']:
        task.session[attr] = task.session[attr] - offset

    # Phase times - all attributes are timestamps
    for attr in task.phase_times.keys():
        task.phase_times[attr] = task.phase_times[attr] - offset

    # Sync - behavioural & neural
    ...

    # Timestamps: pos, rotation, button, encoding, recall, recall_selector_position
    fields = [...]
    for field in fields:
        getattr(task, field)['time'] = getattr(task, field)['time'] - offset

    # Other: ...
    ...

    # Add information to task object about the reset
    task.time_reset = True
    task.time_offset = offset

    return task
