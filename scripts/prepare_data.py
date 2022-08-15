"""Prepare files for conversion."""

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv import process_session
from conv.io import get_files, load_configs, save_config, make_session_name
from conv.utils import print_status

# Import settings (from local folder)
from settings import SUBJ, SETTINGS
from paths import Paths

###################################################################################################
###################################################################################################

def prepare_data(SUBJ=SUBJ, SETTINGS=SETTINGS):
    """Prepare a session of data for NWB conversion."""

    # Initialize paths
    PATHS = Paths(SUBJ['ID'], SUBJ['SESSION'])

    # Define the session name
    session_name = make_session_name(SUBJ['ID'], SUBJ['SESSION'])

    print_status(SETTINGS['VERBOSE'], 'Preparing data for {}'.format(session_name), 0)

    ## PARSE LOG FILE

    if SETTINGS['PARSE_LOG']:

        task = process_session(PATHS, process=True, verbose=SETTINGS['VERBOSE'])
        save_task_object(task, session_name, folder=PATHS.temp)

    ## COLLECT METADATA

    print(SETTINGS['VERBOSE'], 'preparing metadata files...', 1)

    # Get a list of the available metadata files, and load them
    metadata_files = get_files(PATHS.metadata, select='yaml')
    metadata = load_configs(metadata_files, PATHS.metadata)

    # Save out the collected config file for the session
    save_config(metadata, session_name, folder=PATHS.temp)

    print_status(SETTINGS['VERBOSE'], 'Completed data preparation for {}'.format(session_name), 0)


if __name__ == '__main__':
    prepare_data()
