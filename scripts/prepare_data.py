"""Prepare data files to for conversion."""

from pathlib import Path

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv import process_logfile
from conv.io import get_files, load_configs, save_config

# Import settings (from local folder)
from settings import SUBJ, SETTINGS, PATHS, OLD_LOGFILE

###################################################################################################
###################################################################################################

def prepare_data(SUBJ=SUBJ, SETTINGS=SETTINGS, PATHS=PATHS):
    """Prepare a session of data for NWB conversion."""

    if SETTINGS['VERBOSE']:
        print('Preparing data for {}'.format(SUBJ['ID']))

    ## PARSE LOG FILE

    if SETTINGS['PARSE_LOG']:

        if SETTINGS['VERBOSE']:
            print('  processing logfile...')

        task = process_logfile(PATHS['BEHAVIOR'] / 'logfile.txt')

        # Note: conventionalize where this gets saved
        task_name = SUBJ['ID'] + '_' + SUBJ['SESSION'] + '_events.csv'
        save_task_obj(PATHS['SUBJ'] / task_name)


    ## COLLECT METADATA

    if SETTINGS['VERBOSE']:
        print('  preparing metadata files...')

    # Get a list of the available metadata files, and load them
    metadata_files = get_files(PATHS['METADATA'], select='yaml')
    metadata = load_configs(metadata_files, PATHS['METADATA'])

    # Save out the collected config file for the session
    save_config(metadata, SUBJ['ID'] + '_metadata', folder=PATHS['SUBJ'])

    if SETTINGS['VERBOSE']:
        print('Completed data preparation for {}'.format(SUBJ['ID']))


if __name__ == '__main__':
    prepare_data()
