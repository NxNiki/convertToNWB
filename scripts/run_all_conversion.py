"""Run conversion on all sessions."""

import sys
from conv import Paths
from conv.io import get_files, make_session_name
from conv.utils import print_status, catch_error
# Import processing functions (from local scripts)
from prepare_data import prepare_data
from convert_data import convert_data
# Import settings
from conv.settings import PROJECT_PATH, EXPERIMENT, SETTINGS, GROUP, SKIP

sys.path.append('..')


def run_all_conversions():
    """Run NWB conversion on all available TH sessions."""

    msg = '\n\nRUNNING ALL CONVERSIONS FOR - {}\n\n'.format(EXPERIMENT)
    print_status(SETTINGS['VERBOSE'], msg, 0)

    # Initialize paths
    paths = Paths(PROJECT_PATH)

    # Get a list of all available sessions
    all_sessions = {}
    subjects = get_files(paths.recordings)
    for subject in subjects:
        all_sessions[subject] = get_files(paths.recordings / subject / EXPERIMENT, select='session')

    # Get a list of already converted sessions
    converted = get_files(paths.nwb, select='nwb')

    for subject, sessions in all_sessions.items():

        if subject in SKIP['SUBJECTS']:
            print_status(SETTINGS['VERBOSE'], 'SKIPPING SUBJECT: \t{}'.format(subject), 0)
            continue

        for session in sessions:

            # Collect together the subject information & define session ID
            SESSION = {'SUBJECT' : subject, 'EXPERIMENT' : EXPERIMENT, 'SESSION' : session}
            session_name = make_session_name(SESSION['SUBJECT'],
                                             SESSION['EXPERIMENT'],
                                             SESSION['SESSION'])

            # Check for skipping subject
            if session_name in SKIP['SESSIONS']:
                print_status(SETTINGS['VERBOSE'], 'SKIPPING SESSION: \t{}'.format(session_name), 0)
                continue

            # Check for whether to skip already run
            if GROUP['SKIP_ALREADY_RUN'] and session_name + '.nwb' in converted:
                print_status(SETTINGS['VERBOSE'], 'SESSION ALREADY RUN: \t{}'.format(session_name), 0)
                continue

            try:
                # Prepare data
                prepare_data(SESSION=SESSION, SETTINGS=SETTINGS)

                # Run data conversion
                convert_data(SESSION=SESSION, SETTINGS=SETTINGS)

            except Exception as excp:
                catch_error(GROUP['CONTINUE_ON_FAIL'], session_name, paths.nwb / 'zFailed',
                            SETTINGS['VERBOSE'], 'ISSUE CONVERTING SESSION: \t{}')

    msg = '\n\n FINISHED CONVERSIONS FOR - {}\n\n'.format(EXPERIMENT)
    print_status(SETTINGS['VERBOSE'], msg, 0)


if __name__ == '__main__':
    run_all_conversions()
