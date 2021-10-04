"""Check data files."""

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv.io import get_files, make_file_list

# Import settings
from settings import PATHS

###################################################################################################
###################################################################################################

def check_files():
    """Check available data files and conversion status."""

    print('\n\nCHECKING AVAILABLE FILES\n')

    # Check list of available subjects
    subj_files = get_files(PATHS['DATA'], ignore='NWB')

    # Collect the list of data files and NWB files
    sessions = {}
    for subj in subj_files:
        sessions[subj] = get_files(PATHS['DATA'] / subj, select='session')

    # Get list of converted files
    converted = get_files(PATHS['DATA'] / 'NWB')

    # Check the list of available subject & sessions
    print('Available subjects & sessions:')
    for cur_subj, cur_sessions in sessions.items():
        print('\t', cur_subj, '\t', ','.join(cur_sessions))

    # Check the list of converted NWB files
    print('Converted NWB files:')
    for file in converted:
        print('\t {}'.format(file))

    # Check the list of uncoverted files
    not_converted = [file for file in make_file_list(sessions) if file + '.nwb' not in converted]

    # Print out the list of not-converted files
    print('Not yet converted sessions:')
    for file in not_converted:
        print('\t', file)

    print('\n\n')


if __name__ == '__main__':
    check_files()
