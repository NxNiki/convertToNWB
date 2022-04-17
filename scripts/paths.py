"""Path definitions."""

from pathlib import Path

###################################################################################################
###################################################################################################

# Define base data path
DATA_PATH = Path('...')

# Get the location of this file
FILE_PATH = Path(__file__).parent.absolute()
REPO_PATH = FILE_PATH.parent

###################################################################################################
###################################################################################################

class Paths():

    DATA_PATH = DATA_PATH
    REPO_PATH = REPO_PATH

    def __init__(self, subj, session):

        self._subj = subj
        self._session = session

    @property
    def data(self):
        return self.DATA_PATH

    @property
    def session(self):
        return self.data / self._subj / self._session

    @property
    def behavior(self):
        return self.session / 'behavior'

    @property
    def lfp(self):
        return self.session / 'micro_lfp'

    @property
    def neural(self):
        return self.session / 'neural'

    @property
    def spikes(self):
        return self.session / 'spikes'

    @property
    def sync(self):
        return self.session / 'sync'

    @property
    def nwb(self):
        return self.DATA_PATH / 'NWB'

    @property
    def metadata(self):
        return self.REPO_PATH / 'metadata'

    @property
    def temp(self):
        return self.REPO_PATH / 'temp'
