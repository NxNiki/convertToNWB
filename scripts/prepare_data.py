"""Prepare data files to for conversion."""

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv import process_session
from conv.io import get_files, load_configs, save_config

# Import settings (from local folder)
from settings import SUBJ, SETTINGS
from paths import Paths

###################################################################################################
###################################################################################################

def prepare_data(SUBJ=SUBJ, SETTINGS=SETTINGS):
    """Prepare a session of data for NWB conversion."""

    # Initialize paths
    PATHS = Paths(SUBJ['ID'], SUBJ['SESSION'])

    # Define the session ID
    session_id = '_'.join([SUBJ['ID'], SUBJ['SESSION']])

    if SETTINGS['VERBOSE']:
        print('Preparing data for {}'.format(session_id))

    ## PARSE LOG FILE

    if SETTINGS['PARSE_LOG']:

        if SETTINGS['VERBOSE']:
            print('  processing logfile...')

        task = process_session(PATHS.behavior / 'logfile.txt')

        # Add session metadata information
        task.meta['task'] = SUBJ['TASK']
        task.meta['subject'] = SUBJ['ID']
        task.meta['session'] = SUBJ['SESSION']

        # Save out parsed & preprocessed task information
        save_task_obj(task, session_id, folder=PATHS.temp)


    ## COLLECT METADATA

    if SETTINGS['VERBOSE']:
        print('  preparing metadata files...')

    # Get a list of the available metadata files, and load them
    metadata_files = get_files(PATHS.metadata, select='yaml')
    metadata = load_configs(metadata_files, PATHS.metadata)

    # Save out the collected config file for the session
    save_config(metadata, session_id, folder=PATHS.temp)

    if SETTINGS['VERBOSE']:
        print('Completed data preparation for {}'.format(session_id))


if __name__ == '__main__':
    prepare_data()
