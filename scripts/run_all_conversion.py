"""Run conversion on all sessions."""

import sys
sys.path.append('..')
from conv.io import get_files

# Import processing functions (from local scripts)
from prepare_data import prepare_data
from convert_data import convert_data

# Import settings
from settings import SUBJ, SETTINGS, SKIP
from paths import DATA_PATH

###################################################################################################
###################################################################################################

def run_all_conversions():
    """Run NWB conversion on all available TH sessions."""

    print('\n\nRUNNING ALL CONVERSIONS')

    # Get a list of all available sessions
    all_sessions = {}
    subj_files = get_files(DATA_PATH, ignore='NWB')
    for subj in subj_files:
        all_sessions[subj] = get_files(DATA_PATH / subj, select='session')

    for subj, sessions in all_sessions.items():
        for session in sessions:

            # Collect together the subject information & define session ID
            SUBJ = {'ID' : subj, 'SESSION' : session}
            session_id = '_'.join([SUBJ['ID'], SUBJ['SESSION']])

            # Check for skipping subject
            if session_id in SKIP:
                print("SKIPPING SESSION: {}".format(session_id))
                continue

            # Prepare data
            prepare_data(SUBJ=SUBJ, SETTINGS=SETTINGS)

            # Run data conversion
            convert_data(SUBJ=SUBJ, SETTINGS=SETTINGS)

    print('\n\n FINISHED CONVERSIONS{}\n\n')

if __name__ == '__main__':
    run_all_conversions()
