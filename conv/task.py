"""Task class."""

###################################################################################################
###################################################################################################

class Task(object):
    """Object for collecting task data."""

    def __init__(self):
        """Initialize task object."""

        ## TIMING

        self.time = []
        self.sync = []

        ## TASK STRUCTURE

        # Marker variables for particular parts of the task
        self.phase_marker = {...}

        # Information on task elements (navigation / encoding / recall, etc)
        self.task_thing = {...}

        ## POSITION

        self.pos = {'x' : [], 'y' : [], 'z' : []}

        ## BEHAVIOUR

        self.button = {'time' : [], 'x' : [], 'y' : [], 'z' : []}

        ## STIMULI

        self.stim_info = {...}
