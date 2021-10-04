"""Settings for converting data files."""

from pathlib import Path

###################################################################################################
###################################################################################################

#### DEFINE WHETHER TO RUN A TEST RUN

TEST_RUN = False

#### DEFINE SUBJECT INFORMATION

SUBJ_ID = ''
SESSION = ''

#### DEFINE PROPERTIES OF THE SESSION FILE

...

#### DEFINE RUN SETTINGS

PARSE_LOG = True
ADD_LFP = False
VERBOSE = True

#### DEFINE BASE DATA PATH

DATA_PATH = Path('...')

###################################################################################################
## For standard usage, nothing should need to be updated below

#### TEST RUN

# Overide settings of doing test run on local comp
if TEST_RUN:
    DATA_PATH = Path('...')
    SUBJ_ID = 'example'
    SESSION = 'session_0'

#### DEFINE DATA PROPERTIES

# Sampling rates
S_RATE = 30000
S_RATE_FIELD = 500

#### COLLECT SETTINGS INTO COLLECTION OBJECTS

# Get the location of this file
FILE_PATH = Path(__file__).parent.absolute()
REPO_PATH = FILE_PATH.parent

## SUBJECT INFORMATION
SUBJ = {
    'ID' : SUBJ_ID,
    'SESSION' : SESSION
}

## RUN SETTINGS
SETTINGS = {
    'PARSE_LOG' : PARSE_LOG,
    'ADD_LFP' : ADD_LFP,
    'VERBOSE' : VERBOSE
}

## PATH SETTINGS
PATHS = {
    'DATA' : DATA_PATH,
    'BEHAVIOR' : DATA_PATH / SUBJ_ID / SESSION / 'behavioral',
    'SPIKES' : DATA_PATH / SUBJ_ID / SESSION / 'split_files',
    'LFP' : DATA_PATH / SUBJ_ID / SESSION / 'micro_lfp',
    'SYNC' : DATA_PATH / SUBJ_ID / SESSION / 'sync',
    'METADATA' : REPO_PATH / 'metadata',
    'SAVE' : DATA_PATH / 'NWB',
    'SUBJ' : REPO_PATH / 'subject'
}
