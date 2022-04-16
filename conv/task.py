"""Task class."""

from copy import deepcopy

from convnwb.plts import plot_alignment
from convnwb.utils import offset_time, change_time_units

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

        # EXPERIMENT INFORMATION
        self.experiment = {
            'version' : {'label' : None, 'number' : None},
            'language' : None,
            'environment' : {...}
        }

        # SESSION INFORMATION
        self.session = {
            'start' : None,
            'end' : None
        }

        ## SYNCHRONIZATION

        self.sync = {
            ...
        }

        ## TASK STRUCTURE

        # Marker variables for particular parts of the task
        self.phase_times = {
            ...
        }

        ## TRIALS

        # Information on task elements (navigation / encoding / recall, etc)
        self.trial = {
            ...
        }

        ## POSITION

        self.position = {
            'time' : [],
            'x' : [],
            'y' : [],
            'z' : []
        }

        ## BEHAVIOUR

        self.button = {
            # Time of button presses
            'time' : [],
        }

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
    update : {'offset', 'change_units'}
        Label for what kind of update to do to the timestamps.
    kwargs
        Additional arguments to pass to the update function.

    Returns
    -------
    task : Task
        Updated task object.

    Notes
    -----
    This function returns a copy of the task object, so it won't overwrite in place.
    """

    task = deepcopy(task)

    # Select update function to use
    func = {'offset' : offset_time, 'change_units' : change_time_units}[update]

    # Session - session start & end times
    for attr in ['start', 'end']:
        task.session[field] = func(task.session[field], **kwargs)

    # Phase times - all attributes are timestamps
    for attr in task.phase_times.keys():
        task.phase_times[field] = func(task.phase_times[field], **kwargs)

    # Sync - behavioural & neural
    ...

    # Timestamps: ...
    for field in [...]:
        getattr(task, field)['time'] = func(getattr(task, field)['time'], **kwargs)

    # Other: ...
    ...

    # Add information to task object about the reset
    if update == 'offset':
        task.time_reset = True
        task.time_offset = kwargs['offset']

    return task
