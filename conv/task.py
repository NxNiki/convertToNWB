"""Task class."""

from convnwb.task import TaskBase

from convnwb.plts.timestamps import plot_alignment

###################################################################################################
###################################################################################################

class Task(TaskBase):
    """Object for collecting task data."""

    def __init__(self):
        """Initialize task object."""

        # Initialize TaskBase
        super().__init__()

        # Fill in task specific information
        self.sync = {...}
        self.phase_times = {...}
        self.trial = {...}
        self.responses = {...}


    def plot_sync_allignment(self, n_pulses=100):
        """Plots alignment of the synchronization pulses.

        Parameters
        ----------
        n_pulses : int, optional, default: 100
            Number of pulses to plot for zoomed plot.
        """

        raise NotImplementedError
        plot_alignment(self.sync_neural[...],
                       self.sync_behavioral[...],
                       n_pulses=n_pulses)
