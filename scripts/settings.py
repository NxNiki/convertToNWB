"""Settings for converting sessions."""

###################################################################################################
# PATH SETTINGS

PROJECT_PATH = '/Users/XinNiuAdmin/HoffmanMount/data/nwb_projects/movie_paradigm'
NEURALYNX_PATH = '/Volumes/DATA/NLData/'

###################################################################################################
# SUBJECT SETTINGS

SUBJECT = ''
EXPERIMENT = 'movie_paradigm'
SESSION = ''

SESSION = {
    'SUBJECT': SUBJECT,
    'EXPERIMENT': EXPERIMENT,
    'SESSION': SESSION,
}

###################################################################################################
# DEFINE PROPERTIES OF THE SESSION

PROPERTIES = {
    '...': ...,
}

###################################################################################################
# DEFINE RUN SETTINGS

# Logfile settings
PARSE_LOG = False

# Run settings
VERBOSE = True

# Specify what to add to file
ADD_ELECTRODES = False
ADD_UNITS = True
ADD_LFP = False

# Time related settings
RESET_TIME = True
CHANGE_TIME_UNIT = True
DROP_BEFORE_TASK = True

SETTINGS = {
    # Run settings
    'VERBOSE': VERBOSE,

    # Logfile settings
    'PARSE_LOG': PARSE_LOG,

    # What to add
    'ADD_ELECTRODES': ADD_ELECTRODES,
    'ADD_UNITS': ADD_UNITS,
    'ADD_LFP': ADD_LFP,

    # Time related settings
    'RESET_TIME': RESET_TIME,
    'CHANGE_TIME_UNIT': CHANGE_TIME_UNIT,
    'DROP_BEFORE_TASK': DROP_BEFORE_TASK,
}

###################################################################################################
# DEFINE GROUP LEVEL SETTINGS

SKIP_ALREADY_RUN = False
CONTINUE_ON_FAIL = False

GROUP = {

    'SKIP_ALREADY_RUN': SKIP_ALREADY_RUN,
    'CONTINUE_ON_FAIL': CONTINUE_ON_FAIL,

}

###################################################################################################
# DEFINE SKIP SESSIONS

SKIP_SUBJECTS = [
    '...',
]

SKIP_SESSIONS = [
    '...',
]

SKIP = {
    'SUBJECTS': SKIP_SUBJECTS,
    'SESSIONS': SKIP_SESSIONS,
}
