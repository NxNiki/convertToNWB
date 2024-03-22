"""Convert a session of data to NWB."""

import numpy as np

from pynwb import NWBFile, TimeSeries, ProcessingModule
from pynwb.file import Subject, Units
from pynwb.behavior import Position
from pynwb.ecephys import ElectricalSeries

# Add local folder with `conv` module
import sys
sys.path.append('..')
from conv import Paths, Electrodes
from conv.io import (get_files, make_session_name, load_config,
                     load_task_object, open_h5file, save_nwbfile)
from conv.utils import print_status, incrementer, get_current_date, convert_time_to_date

# Import settings (from local folder)
from conv.settings import PROJECT_PATH, SESSION, SETTINGS

###################################################################################################
###################################################################################################

def convert_data(SESSION=SESSION, SETTINGS=SETTINGS):
    """Convert a session of data to an NWB file."""

    # Initialize paths
    paths = Paths(PROJECT_PATH, SESSION['SUBJECT'], SESSION['EXPERIMENT'], SESSION['SESSION'])

    # Define the session name
    session_name = make_session_name(SESSION['SUBJECT'], SESSION['EXPERIMENT'], SESSION['SESSION'])

    print_status(SETTINGS['VERBOSE'], '\nCONVERTING XX DATA\n', 0)
    print_status(SETTINGS['VERBOSE'], 'Converting data for: \t{}'.format(session_name), 0)

    ## FILE LOADING

    # Load behavior data
    task = load_task_object(session_name, folder=paths.task)
    assert task

    # Load metadata file
    metadata = load_config(session_name, folder=paths.metadata)
    assert metadata

    # Load the electrode information
    electrodes = Electrodes()
    # If there is detailed electrode information to load, do so here
    if SETTINGS['ADD_ELECTRODES']:
        pass
    # Otherwise, define a placeholder electrodes object
    else:
        electrodes.set_placeholder()

    # Get a list of the available spike files
    if SETTINGS['ADD_UNITS']:

        spike_files = get_files(paths.spikes, 'XX')
        assert len(spike_files)

    # Get the list of available LFP files
    if SETTINGS['ADD_LFP']:

        lfp_files = get_files(paths.micro_lfp, ext='.p')
        assert lfp_files

    ## SETUP

    # Initialize notes
    notes = None

    # Get the session date
    session_date = convert_time_to_date(task.session['start_time'] / 1000)

    # Define collection site information
    if SESSION['SUBJECT'][:] == '':
        data_collection = 'XX'
    else:
        data_collection = 'unknown'

    if SETTINGS['CHANGE_TIME_UNIT']:

        # Convert timestamp units, from milliseconds to seconds
        task.update_time('change_units', value=1000, operation='divide')

    if SETTINGS['RESET_TIME']:

        # Reset task time stamps to start at the session start time
        task.update_time('offset', offset=task.session['start_time'])
        notes = 'The exact subtracted timestamp is: {}'.format(task.info['time_offset'])

    ## INITIALIZE NWB FILE

    # Create subject object
    age = metadata['subject']['age'] if metadata['subject']['age'] != 'XX' else None
    sex = metadata['subject']['sex'] if metadata['subject']['sex'] != 'XX' else None
    subject = Subject(subject_id=SESSION['SUBJECT'], age=age, sex=sex,
                      species=metadata['subject']['species'],
                      description=metadata['subject']['description'])

    # Define information for initializing NWBfile
    experiment_description = \
        'Task: ' + task.experiment['version']['label'] + \
        ' build-' + task.experiment['version']['number'] + \
        ' ({})'.format(task.experiment['language'])

    # Initialize a NWB file
    nwbfile = NWBFile(session_description=metadata['study']['session_description'],
                      identifier=metadata['study']['identifier'],
                      file_create_date=get_current_date(),
                      session_start_time=session_date,
                      experimenter=metadata['study']['experimenter'],
                      experiment_description=experiment_description,
                      session_id=session_name,
                      institution=metadata['study']['institution'],
                      keywords=metadata['study']['keywords'],
                      notes=notes,
                      source_script=metadata['study']['source_script'],
                      source_script_file_name='scripts/' + __file__,
                      data_collection=data_collection,
                      stimulus_notes=metadata['study']['stimulus_notes'],
                      lab=metadata['study']['lab'],
                      subject=subject)

    ## RECORDING DEVICE INFORMATION

    if SETTINGS['ADD_ELECTRODES'] or SETTINGS['ADD_UNITS']:

        # Create device object
        device = nwbfile.create_device(metadata['device']['device_name'],
                                       metadata['device']['device_description'],
                                       metadata['device']['device_manufacturer'])

        # Add electrode bundles and electrode information
        for bundle_name, bundle_location in electrodes:

            # Create an electrode group for the current bundle
            electrode_group = nwbfile.create_electrode_group(name=bundle_name,
                                                             description=metadata['device']['bundle_description'],
                                                             location=bundle_location,
                                                             device=device)

            # Add electrodes to file for the current bundle
            for electrode_ind in range(electrodes.n_electrodes_per_bundle):
                nwbfile.add_electrode(location=electrode_group.location,
                                      group=electrode_group,
                                      id=electrode_ind, enforce_unique_id=False)

    ## STIMULUS INFORMATION

    # Add stimulus information here...
    # Depending on the task, this could included using:
    # nwbfile.stimulus (with `add_stimulus`), which can contain stimuli such as images
    # nwbfile.acquisition (with `add_acquisition`), which can contain information such as positions

    # Add stimuli information to file, as NWB stimulus objects
    #   In this case, `add_stimulus` expect to add a series of TimeSeries objects - could be images, etc
    stimuli = ...      # Load or define stimuli (load might want to move to top)
    for stim in stimuli:
        nwbfile.add_stimulus(stim)
    # AND/OR
    # Add stimulus position information
    stimuli = Position(name='stimuli')
    stimuli.create_spatial_series(name='stimulus_positions',
                                  data=task.stimuli['...'],
                                  unit='virtual units',
                                  reference_frame='corner',
                                  rate=0.,
                                  description=metadata['stimulus']['...'])
    nwbfile.add_acquisition(stimuli)

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
                              stop_time=task...)
        except IndexError:
            print_status(SETTINGS['VERBOSE'], 'Incomplete last trial - skipped adding.', 1)

    ## POSITION DATA

    # Define and add the boundary definitions
    boundaries = Position(name='boundaries')
    boundaries.create_spatial_series(name='arena_center',
                                     data=np.array([task.environment['...'],
                                                    task.environment['...']]),
                                     unit='virtual units',
                                     reference_frame='corner',
                                     rate=0.,
                                     description=metadata['position']['arena_center'])
    boundaries.create_spatial_series(name='arena_x_range',
                                     data=np.array([task.environment['...'],
                                                    task.environment['...']]),
                                     unit='virtual units',
                                     reference_frame='corner',
                                     rate=0.,
                                     description=metadata['position']['arena_x_range'])
    boundaries.create_spatial_series(name='arena_z_range',
                                     data=np.array([task.environment['...'],
                                                    task.environment['...']]),
                                     unit='virtual units',
                                     reference_frame='corner',
                                     rate=0.,
                                     description=metadata['position']['arena_z_range'])
    nwbfile.add_acquisition(boundaries)

    # Set position data as a spatial series and add to NWB file
    position = Position(name='position')
    position.create_spatial_series(name='player_position',
                                   data=np.vstack([task.position['x'], task.position['z']]),
                                   unit='virtual units',
                                   timestamps=task.position['time'],
                                   reference_frame='middle',
                                   description=metadata['position']['player_position'])
    nwbfile.add_acquisition(position)

    # Set head direction information as a compass direction and add to NWB file
    head_direction = CompassDirection(name='head_direction')
    head_direction.create_spatial_series(name='head_direction',
                                         data=task.head_direction['degrees'],
                                         unit='degrees',
                                         timestamps=task.head_direction['time'],
                                         reference_frame='north',
                                         description=metadata['position']['head_direction'])
    nwbfile.add_acquisition(head_direction)

    # Create time series for speed & linear position
    speed = TimeSeries(name='speed',
                       data=task.position['speed'],
                       unit='virtual units / second',
                       timestamps=task.position['time'],
                       description=metadata['position']['speed'])

    # Add derived spatial measures to NWB file as ProcessingModule
    position_derivatives = ProcessingModule(name='position_measures',
                                            data_interfaces=[speed],
                                            description=metadata['position']['derived_position_measures'])
    nwbfile.add_processing_module(position_derivatives)

    ## UNIT DATA

    if SETTINGS['ADD_UNITS']:

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
        ind = incrementer()
        for spike_file in enumerate(spike_files):

            # Get channel information from file name
            channel = ...

            # Load spike file & get spike data (example for HDF5 files)
            with open_h5file(spike_file, paths.spikes) as h5file:

                spike_data = h5file['spike_data_sorted']
                spike_times = spike_data['spike_times'][:]
                spike_clusters = spike_data['spike_clusters'][:]
                spike_waveforms = spike_data['spike_waveforms'][:]

            # If task information has been offset, apply the same to spike times
            if task.status['time_reset']:
                spike_times = spike_times - task.info['time_offset']

            # Loop across clusters within the file, and add each unit
            for cluster in set(spike_clusters):
                mask = spike_clusters == cluster

                # Get the spike times for the cluster
                unit_spike_times = spike_times[mask]
                if SETTINGS['DROP_BEFORE_TASK']:
                    unit_spike_times = unit_spike_times[unit_spike_times >= task.session['start_time']]

                # Get the average waveform
                unit_waveform_mean = np.mean(spike_waveforms[mask, :], 0)

                # Add unit data
                nwbfile.add_unit(id=next(ind),
                                 electrodes=[0],
                                 channel=channel,
                                 location=...,
                                 waveform_mean=unit_waveform_mean,
                                 spike_times=unit_spike_times)

    ## FIELD DATA

    if SETTINGS['ADD_LFP']:

        # Create the electrode table
        electrode_table_region = nwbfile.create_electrode_table_region([0], 'xx')

        # Add each LFP trace as a new object
        for ind, lfp_file in enumerate(lfp_files):
            with open(paths.lfp / lfp_file, 'rb') as pfile:

                # Load ephys data
                ephys_data = load(...)

                # Create & add electrical series to store LFP data
                ephys_ts = ElectricalSeries('field_data_' + str(ind),
                                            ephys_data,
                                            electrode_table_region,
                                            starting_time=0.,    # Might need update this
                                            rate=...,            # Need to add this somewhere
                                            resolution=np.inf,
                                            comments="...",
                                            description="LFP time series.")
                nwbfile.add_acquisition(ephys_ts)

    ## FINISH

    # Save out NWB file
    save_nwbfile(nwbfile, session_name, folder=paths.nwb)

    print_status(SETTINGS['VERBOSE'], 'Data converted for: \t{}'.format(session_name), 0)


if __name__ == '__main__':
    convert_data()
