"""Prepare files for conversion."""

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv import Paths, process_session
from conv.io import get_files, make_session_name, load_configs, save_config, save_task_object
from conv.utils import print_status

# Import settings (from local folder)
from settings import PROJECT_PATH, SESSION, SETTINGS

###################################################################################################
###################################################################################################

def prepare_data(SESSION=SESSION, SETTINGS=SETTINGS):
    """Prepare a session of data for NWB conversion."""

    # Initialize paths
    paths = Paths(PROJECT_PATH, SESSION['SUBJECT'], SESSION['EXPERIMENT'], SESSION['SESSION'])

    # Define the session name
    session_name = make_session_name(SESSION['SUBJECT'], SESSION['EXPERIMENT'], SESSION['SESSION'])

    print_status(SETTINGS['VERBOSE'], '\nPREPARING XX DATA\n', 0)
    print_status(SETTINGS['VERBOSE'], 'Preparing data for {}'.format(session_name), 0)

    ## PARSE LOG FILE

    if SETTINGS['PARSE_LOG']:

        task = process_session(paths, process=True, verbose=SETTINGS['VERBOSE'])
        save_task_object(task, session_name, folder=paths.task)

    ## COLLECT METADATA

    print(SETTINGS['VERBOSE'], 'preparing metadata files...', 1)

    # Get a list of the available metadata files, and load them
    metadata_files = get_files('../metadata/', select='yaml')
    metadata = load_configs(metadata_files, '../metadata/')

    # Save out the collected config file for the session
    save_config(metadata, session_name, folder=paths.metadata)

    print_status(SETTINGS['VERBOSE'],
                 'Completed data preparation for {}\n'.format(session_name), 0)


if __name__ == '__main__':
    prepare_data()
