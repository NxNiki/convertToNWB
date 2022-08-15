"""Settings for converting sessions."""

###################################################################################################
###################################################################################################

#### DEFINE TASK

TASK = ''

#### DEFINE SUBJECT INFORMATION

SUBJ_ID = ''
SESSION = ''

#### DEFINE PROPERTIES OF THE SESSION FILE

...

#### DEFINE RUN SETTINGS

PARSE_LOG = True
ADD_LFP = False
RESET_TIME = True
CHANGE_TIME_UNIT = True
DROP_BEFORE_TASK = True
VERBOSE = True

#### DEFINE SKIP SESSIONS

SKIP = []

###################################################################################################
## For standard usage, nothing should need to be updated below

#### COLLECT SETTINGS INTO COLLECTION OBJECTS

## SUBJECT INFORMATION
SUBJ = {
    'TASK' : TASK,
    'ID' : SUBJ_ID,
    'SESSION' : SESSION
}

## RUN SETTINGS
SETTINGS = {
    'PARSE_LOG' : PARSE_LOG,
    'ADD_LFP' : ADD_LFP,
    'RESET_TIME' : RESET_TIME,
    'CHANGE_TIME_UNIT' : CHANGE_TIME_UNIT,
    'DROP_BEFORE_TASK' : DROP_BEFORE_TASK,
    'VERBOSE' : VERBOSE
}
