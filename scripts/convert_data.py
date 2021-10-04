"""Convert a data file to NWB."""

from datetime import datetime
from dateutil.tz import tzlocal

import h5py
import numpy as np

from pynwb import NWBFile, NWBHDF5IO, TimeSeries, ProcessingModule
from pynwb.file import Subject
from pynwb.behavior import Position, SpatialSeries
from pynwb.ecephys import ElectricalSeries, SpikeEventSeries

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv.io import get_files, load_config
from conv.utils import clean_strings, get_event_time

# Import settings
from settings import SUBJ, PATHS, SETTINGS

###################################################################################################
###################################################################################################

def convert_data(SUBJ=SUBJ, PATHS=PATHS, SETTINGS=SETTINGS):
    """Convert a session of data to an NWB file."""

    if SETTINGS['VERBOSE']:
        print('Converting data for {}'.format(SUBJ['ID']))

    ## SETUP & FILE LOADING

    # Get current date
    current_date = datetime.now(tzlocal())

    # Load behavior data
    task = load_task_obj(SUBJ['ID'] + '_' + SUBJ['SESSION'] + '_task.p')

    # Load metadata file
    metadata = load_config(SUBJ['ID'] + '_metadata.yaml', folder=PATHS['SUBJ'])

    # Define collection site information
    if SUBJ['ID'][::] == '':
        data_collection = 'XX'
    else:
        data_collection = 'unknown'

    ## INITIALIZE NWB FILE

    # Create subject object
    subject = Subject(age=metadata['subject']['age'],
                      sex=metadata['subject']['sex'],
                      description=metadata['subject']['description'],
                      species=metadata['subject']['species'],
                      subject_id=SUBJ['ID'])

    # Initialize a NWB file
    nwbfile = NWBFile(session_description=metadata['study']['session_description'],
                      identifier=metadata['study']['identifier'],
                      file_create_date=current_date,
                      session_start_time=current_date,
                      session_start_time=metadata['study']['session_start_time'],
                      experimenter=metadata['study']['experimenter'],
                      lab=metadata['study']['lab'],
                      institution=metadata['study']['institution'],
                      data_collection=data_collection,
                      experiment_description=metadata['study']['experiment_description'],
                      subject=subject,
                      session_id=SUBJ['ID'] + '-' + SUBJ['SESSION'])


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
    n_electrodes = 5
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

    # Add event defintions
    for event, description in metadata['events'].items():
        nwbfile.add_trial_column(event, description)

    # Collect trial indices
    trial_inds = ...

    # Get all trial start & stop times
    trial_start_times = times[np.hstack([np.array([0]), trial_inds[:-1]])]
    trial_stop_times = times[trial_inds-1]

    # Add event information to NWB file
    n_trials = len(trial_inds)
    for t_ind in range(n_trials):

        # Get trial start and end times
        t_start = trial_start_times[t_ind]
        t_end = trial_stop_times[t_ind]

        # Add trial information to file
        nwbfile.add_trial(start_time=t_start,
                          ...,
                          stop_time=t_end
                          )


    ## POSITION DATA

    # Get location data
    times = task.aligned_times
    loc_data = np.vstack([task.pos['x'], task.pos['z']])

    # Set position data as a spatial series and add to NWB file
    position = Position(name='position')
    position.create_spatial_series(name='xy_position',
                                   data=loc_data,
                                   timestamps=times,
                                   reference_frame='middle',
                                   description='XY position of the subject along the track.')
    nwbfile.add_acquisition(position)

    # Create time series for speed & linear positon
    speed = TimeSeries(name='speed',
                       data=np.array(task.pos['speed']),
                       unit='virtual units / second',
                       timestamps=times)

    # Add derived spatial measures to NWB file as ProcessingModule
    position_things = ProcessingModule(name='position_measures',
                                       description='Derived measures related to position data.',
                                       data_interfaces=[speed])
    nwbfile.add_processing_module(position_things)


    ## UNIT DATA

    # Get a list of the available spike files
    spike_files = get_files(PATHS['SPIKES'], 'times_')

    # Check that there are spike files available
    if len(spike_files) == 0:
        raise ValueError('No split spike time files found - cannot proceed.')

    # Specify additional metadata columns for units
    nwbfile.add_unit_column('channel', 'The recording channel of this unit.')
    nwbfile.add_unit_column('location', 'The anatomical location of this unit.')

    # Add each unit to the NWB file
    for ind, spike_file in enumerate(spike_files):

        # Get channel information from file name
        channel = spike_file.split('.')[0].split('_')[-1]

        # Load spike file & get spike data
        # NOTE: currently loads HDF5 file - update as needed
        with h5py.File(PATHS['SPIKES'] / spike_file, 'r') as h5file:
            spike_data = h5file['spike_data_sorted']

            # Add unit data
            nwbfile.add_unit(id=ind,
                             electrodes=[0],
                             channel=channel,
                             waveform_mean=np.mean(spike_data['spikeWaveforms'][:], 0),
                             spike_times=spike_data['spikeTimes'][:])

    ## FIELD DATA

    if SETTINGS['ADD_LFP']:

        # Create the electrode table
        electrode_table_region = nwbfile.create_electrode_table_region([0], 'xx')

        # Get the list of available LFP files
        lfp_files = get_files(PATHS['LFP'], ext='.p')

        # Add each LFP trace as a new object
        for ind, lfp_file in enumerate(lfp_files):
            with open(PATHS['LFP'] / lfp_file, 'rb') as pfile:

                # Load ephys data
                #ephys_data = load(...)

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
    #   Note: upcoming PYNWB supports Path objects. Until then, typecast to str
    save_name = SUBJ['ID'] + '_' + SUBJ['SESSION'] + '.nwb'
    with NWBHDF5IO(str(PATHS['SAVE'] / save_name), 'w') as io:
        io.write(nwbfile)

    if SETTINGS['VERBOSE']:
        print('Data converted for {}'.format(SUBJ['ID']))


if __name__ == '__main__':
    convert_data()
