import os.path
from datetime import datetime
from dateutil import tz
from pathlib import Path
from neuroconv.datainterfaces import NeuralynxRecordingInterface


ECEPHY_DATA_PATH = "/Users/XinNiuAdmin/Documents/NWBTest"
OUTPUT_PATH = f"{ECEPHY_DATA_PATH}/output"

path_to_save_nwbfile = f"{OUTPUT_PATH}/test_nwb.nwb"
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

# For this data interface we need to pass the folder where the data is
folder_path = f"{ECEPHY_DATA_PATH}/"
# Change the folder_path to the appropriate location in your system
interface = NeuralynxRecordingInterface(folder_path=folder_path, verbose=True)

# Extract what metadata we can from the source files
metadata = interface.get_metadata()
# session_start_time is required for conversion. If it cannot be inferred
# automatically from the source files you must supply one.
session_start_time = metadata["NWBFile"]["session_start_time"]
session_start_time = session_start_time.replace(tzinfo=tz.gettz("US/Pacific"))
metadata["NWBFile"]["session_start_time"] = session_start_time

 # Choose a path for saving the nwb file and run the conversion
nwbfile_path = f"{path_to_save_nwbfile}"  # This should be something like: "./saved_file.nwb"
interface.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
