"""Functions for parsing log files."""

# Import local code
from conv.task import Task
from conv.process import process_task
from conv.utils import print_status


def process_session(paths, process=False, task=None, verbose=True):
    """Process a session of data.

    Parameters
    ----------
    paths : Paths
        Paths object.
    process : bool, optional, default: False
        Whether to process the collected task information.
    task : Task, optional
        Task object to use.
    verbose : bool, optional, default: True
        Whether to print out updates.

    Returns
    -------
    task : Task
        Task event containing parsed logfile information.
    """

    # Create task structure
    if task is None:
        task = Task()

    # Add metadata information to task object
    task.add_metadata(paths._subject, paths._experiment, paths._session)

    # Parse the log file
    task = parse_lines_log(paths.behavior / 'logfile.txt', task=task)

    if process:
        task = process_task(task)

    return task


def parse_lines_log(file_path, task=None, verbose=True):
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

    print_status(verbose, 'parsing logfile...', 2)

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

        #  Get the start & end times of the session, and count number of lines
        lines = fobj.readlines()
        task.session['start_time'] = lines[0].split('\t')[0]
        task.session['end_time'] = lines[-1].split('\t')[0]
        n_lines = len(lines)

        # Reset file object to the start of the file
        fobj.seek(0)

        for ix, line in enumerate(fobj.readlines()):

            # ------ SETUP ------
            line = line.replace('\r', '')
            tokens = line[:-1].split('\t')

            # Check for lines that seem to have an issue
            if len(tokens) <= 3:
                print('Unexpected line length at line {}'.format(ix))
                continue

            # Parse consistent variables
            time = tokens[0]
            frame = tokens[1]
            event = tokens[2]
            subevent = tokens[3]

            ## ------ WORDS WORDS WORDS ------
            if event == 'THINGS':
                ...

            ## ------ WORDS WORDS WORDS ------
            if event == 'THINGS':
                ...


    return task


def parse_lines_sync(file_path, task=None, verbose=True):
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

    print_status(verbose, 'parsing sync...', 2)

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
