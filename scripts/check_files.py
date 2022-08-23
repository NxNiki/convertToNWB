"""Check data files."""

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv import Paths
from conv.io import get_files, make_file_list, missing_files
from convth.utils import print_status

# Import settings
from settings import PROJECT_PATH, EXPERIMENT

###################################################################################################
###################################################################################################

def check_files():
    """Check available data files and conversion status."""

    print_status(True, '\nCHECKING AVAILABLE FILES - {}'.format(EXPERIMENT), 0)

    paths = Paths(PROJECT_PATH)

    # Check list of available subjects
    subjects = get_files(paths.recordings)

    # Collect the list of data files and NWB files
    sessions = {}
    for subject in subjects:
        sessions[subject] = get_files(paths.recordings / subject / EXPERIMENT, select='session')

    # Get list of converted files
    converted = get_files(paths.nwb, select=EXPERIMENT)

    # Check the list of available subject & sessions
    print('Available subjects & sessions:')
    for cur_subj, cur_sessions in sessions.items():
        print_status(True, cur_subj + '\t' + ', '.join(cur_sessions), 1)

    # Check the list of converted NWB files
    print('Converted NWB files:')
    for file in converted:
        print_status(True, file, 1)

    # Check the list of uncoverted files
    file_list = make_file_list(EXPERIMENT, sessions, '.nwb')
    not_converted = missing_files(file_list, converted)

    # Print out the list of not-converted files
    print('Not yet converted sessions:')
    for file in not_converted:
        print_status(True, file, 1)

    print_status(True, '\n\n', 0)


if __name__ == '__main__':
    check_files()
