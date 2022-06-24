"""Convert a session of data to NWB."""

from pathlib import Path
from datetime import datetime
from dateutil.tz import tzlocal

import h5py
import numpy as np

from pynwb import NWBFile, TimeSeries, ProcessingModule
from pynwb.file import Subject
from pynwb.behavior import Position, SpatialSeries
from pynwb.ecephys import ElectricalSeries, SpikeEventSeries

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv.io import get_files, load_config, make_session_name, save_nwbfile

# Import settings (from local folder)
from settings import SUBJ, SETTINGS
from paths import Paths

###################################################################################################
###################################################################################################

def convert_data(SUBJ=SUBJ, SETTINGS=SETTINGS):
    """Convert a session of data to an NWB file."""

    # Initialize paths
    PATHS = Paths(SUBJ['ID'], SUBJ['SESSION'])

    # Define the session name
    session_name = make_session_name(SUBJ['ID'], SUBJ['SESSION'])

    if SETTINGS['VERBOSE']:
        print('Converting data for: {}'.format(session_name))

    ## FILE LOADING

    # Load behavior data
    task = load_task_obj(session_name, folder=PATHS.temp)
    assert task

    # Load metadata file
    metadata = load_config(session_name, folder=PATHS.temp)
    assert metadata

    # Get a list of the available spike files
    spike_files = get_files(PATHS.spikes, 'XX')
    assert len(spike_files)

    # Get the list of available LFP files
    if SETTINGS['ADD_LFP']:
        lfp_files = get_files(PATHS.lfp, ext='.p')
        assert lfp_files

    ## SETUP

    # Get current date
    current_date = datetime.now(tzlocal())

    # Initialize notes
    notes = None

    # Get the session date
    session_date = datetime.fromtimestamp(task.session['start'] / 1000, tz=tzlocal())

    # Define collection site information
    if SUBJ['ID'][::] == '':
        data_collection = 'XX'
    else:
        data_collection = 'unknown'

    if SETTINGS['CHANGE_TIME_UNIT']:

        # Convert timestamp units, from milliseconds to seconds
        task = update_task_time(task, 'change_units', value=1000, operation='divide')

    if SETTINGS['RESET_TIME']:

        # Reset task time stamps to start at the session start time
        task = update_task_time(task, 'offset', offset=task.session['start'])
        notes = 'The exact subtracted timestamp is: {}'.format(task.time_offset)

    ## INITIALIZE NWB FILE

    # Create subject object
    age = metadata['subject']['age'] if metadata['subject']['age'] != 'XX' else None
    sex = metadata['subject']['sex'] if metadata['subject']['sex'] != 'XX' else None
    subject = Subject(subject_id=SUBJ['ID'], age=age, sex=sex,
                      species=metadata['subject']['species'],
                      description=metadata['subject']['description'])

    # Define information for initializing NWBfile
    experiment_description = \
        'Task: ' + task.experiment['version']['label'] + \
        ' build-' + task.experiment['version']['number'] + \
        ' ({})'.format(task.experiment['language'])

    # Get script path - defined as script name + parent directory (folder within repo)
    script_path = Path(__file__)
    source_file_name = str(script_path.parents[0] / script_path.name)

    # Initialize a NWB file
    nwbfile = NWBFile(session_description=metadata['study']['session_description'],
                      identifier=metadata['study']['identifier'],
                      file_create_date=current_date,
                      session_start_time=session_date,
                      experimenter=metadata['study']['experimenter'].split(','),
                      experiment_description=experiment_description,
                      session_id=session_name,
                      institution=metadata['study']['institution'],
                      keywords=metadata['study']['keywords'].split(','),
                      notes=notes,
                      source_script=metadata['study']['source_script'],
                      source_script_file_name=source_file_name,
                      data_collection=data_collection,
                      stimulus_notes=metadata['study']['stimulus_notes'],
                      lab=metadata['study']['lab'],
                      subject=subject)

    ## RECORDING DEVICE INFORMATION

    # Create device object
    device = nwbfile.create_device(metadata['device']['name'],
                                   metadata['device']['description'],
                                   metadata['device']['manufacturer'])

    # Electrodes - add electrode description
    electrode_name = '{}-microwires-{}'.format('A', 'chnum')
    location = metadata['electrode']['location']
    description = metadata['electrode']['location']

    # Add electrode group
    electrode_group = nwbfile.create_electrode_group(electrode_name, \
        description=description, location=location, device=device)

    # Define / get electrode information
    x_pos, y_pos, z_pos = 0.0, 0.0, 0.0
    imp = np.nan
    location = 'place'
    filtering = '0, np.inf'
    reference = None

    # Add electrode to NWB
    n_electrodes = 8
    for ind in range(n_electrodes):
        nwbfile.add_electrode(x_pos, y_pos, z_pos, imp, location,
                              filtering, electrode_group,
                              id=ind, reference=reference)

    ## STIMULUS INFORMATION

    # Add stimuli information to file, as NWB stimulus objects
    stim_description = 'DESCRIPTION.'
    for stim in stimuli:
        nwbfile.add_stimulus(stim)


    ## BEHAVIOURAL DATA

    # Add event definitions
    for event, description in metadata['events'].items():
        nwbfile.add_trial_column(event, description)

    # Add event information to NWB file
    for t_ind in range(len(task.trial['trial'])):

        # Add trial information to file
        try:
            nwbfile.add_trial(start_time=task...,
                              ...,
                              stop_time=task...
                              )
        except IndexError:
            print('\tIncomplete last trial - skipped adding.')


    ## POSITION DATA

    # Set position data as a spatial series and add to NWB file
    position = Position(name='position')
    position.create_spatial_series(name='player_position',
                                   data=np.vstack([task.position['x'], task.position['z']]),
                                   unit='virtual units',
                                   timestamps=task.position['time'],
                                   reference_frame='middle',
                                   description='Position of the subject along the track.')
    nwbfile.add_acquisition(position)

    # Create time series for speed & linear position
    speed = TimeSeries(name='speed',
                       description='The players movement speed, computed from the position data.',
                       data=task.position['speed'],
                       unit='virtual units / second',
                       timestamps=task.position['time'])

    # Add derived spatial measures to NWB file as ProcessingModule
    position_things = ProcessingModule(name='position_measures',
                                       description='Derived measures related to position data.',
                                       data_interfaces=[speed])
    nwbfile.add_processing_module(position_things)


    ## UNIT DATA

    # Define some sorting metadata
    description = "Spike sorting solutions - done with {} (v-{}) by {}.".format(\
        metadata['sorting']['sorter'],
        metadata['sorting']['version'],
        metadata['sorting']['done_by'])

    # Initialize the units data, with given description
    nwbfile.units = Units('units', description=description)

    # Add unit metadata columns
    for field, description in metadata['units'].items():
        nwbfile.add_unit_column(field, description)

    # Add each unit to the NWB file
    for ind, spike_file in enumerate(spike_files):

        # Load spike file & get spike data (example for HDF5 files)
        with h5py.File(PATHS.spikes / spike_file, 'r') as h5file:

            spike_data = h5file['spike_data_sorted']

            # Add unit data
            nwbfile.add_unit(id=ind,
                             electrodes=[0],
                             channel=...,
                             location=...,
                             spike_times=...
                             )

    ## FIELD DATA

    if SETTINGS['ADD_LFP']:

        # Create the electrode table
        electrode_table_region = nwbfile.create_electrode_table_region([0], 'xx')

        # Add each LFP trace as a new object
        for ind, lfp_file in enumerate(lfp_files):
            with open(PATHS.lfp / lfp_file, 'rb') as pfile:

                # Load ephys data
                ephys_data = load(...)

                # Create & add electrical series to store LFP data
                ephys_ts = ElectricalSeries('field_data_' + str(ind),
                                            ephys_data,
                                            electrode_table_region,
                                            starting_time=0.,  # TO CHECK
                                            rate=S_RATE_FIELD,
                                            resolution=np.inf,
                                            comments="...",
                                            description="LFP time series.")
                nwbfile.add_acquisition(ephys_ts)

    ## FINISH

    # Save out NWB file
    save_nwbfile(nwbfile, session_name, folder=PATHS.nwb)

    if SETTINGS['VERBOSE']:
        print('Data converted for: {}'.format(session_name))


if __name__ == '__main__':
    convert_data()
