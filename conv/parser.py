"""Functions for parsing log files."""

# Import local code
from conv.task import Task
from conv.process import process_task

###################################################################################################
###################################################################################################

def process_session(file_path_log, process=False):
    """Process a session of data.

    Parameters
    ----------
    file_path_log : str or Path
        Path to the task logfile.
    process : bool, optional, default: False
        Whether to process the collected task information.

    Returns
    -------
    task : Task
        Task event containing parsed logfile information.
    """

    # Create task structure
    if task is None:
        task = Task()

    # Parse the log file
    task = parse_lines_log(file_path)

    if verbose:
        print('\tparsing completed...')

    if process:
        task = process_task(task)

    return task


def parse_lines_log(file_path, task=None):
    """Parse the lines of a task log file, collecting information into a Task object.

    Parameters
    ----------
    file_path : str or Path
        The path to the log file to parse information from.

    Returns
    -------
    task : Task
        Task event containing parsed logfile information.
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
    """"Parse timestamp information from a synchronization file.

    Parameters
    ----------
    file_path : str or Path
        The path to the sync file.

    Returns
    -------
    task : Task
        Task event containing parsed syncfile information.
    """

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
