"""Functions to work with managing timestamps."""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

###################################################################################################
###################################################################################################

def align_times(sync_nsp, sync_behavioral, logtimes):
    """Align times across different recording systems.

    Parameters
    ----------
    sync_nsp : 1d array
        Synchronization times from the NSP.
    sync_behavioural : 1d array
        Synchronization times from the behavioural computer.
    logtimes : 1d array
        Times from the logfile.

    Returns
    -------
    aligned_times : 1d array
        Aligned behavioural times that match the clock time of the spikes.

    Notes
    -----
    XXXXX
    """

    # Organize data arrays, and divide by sampling rates - CHECK
    sync_nsp = np.array(sync_nsp).astype(float).reshape(-1, 1) / 30000
    sync_behavioral = np.array(sync_behavioral).astype(float).reshape(-1, 1) / 1000

    # Linear model to predict alignment between time traces
    x_train, x_test, y_train, y_test = train_test_split(sync_behavioral, (sync_nsp),
                                                        test_size=0.50, random_state=42)

    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    # Test the alignment between sync timestamps
    score = r2_score(y_test, y_pred)
    if score < 0.99:
        raise ValueError('This session has bad synchronization between brain and behavior')

    # Use the linear model to get aligned times
    aligned_times = model.predict(np.array(logtimes).astype(float).reshape(-1, 1) / 1000) * 1000

    return aligned_times
