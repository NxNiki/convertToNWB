# ConvertTEMPLATE

Template structure for converting data to NWB format.

## Overview

This repository provides a template for managing and converting data files into the
[neurodata without borders](https://www.nwb.org/) format.

Specifically, this template is for converting data in which single-unit data (from microwires)
has been recorded along with a task for which behavioural data and task information has been logged.

To do so, this template includes:

- metadata information and prompts required for data conversion
- code for parsing task logfiles & organizing data
- basic utilities for preprocessing and aligning data
- scripts templates to apply conversion procedures to collected data files

Note that this template / procedure does not include any processing of the data, such as spike sorting.
Any such processing and analysis steps should be done separate to this data conversion (and can be applied before or after).

## How to use this template

In order to apply this template to a new task, the following updates are needed:

- metadata, including required fields and event information, need to be defined
- the parser and task code need to customized for the task
- data files need to organized into a systematic file organization
- preprocessing procedures to be applied during the conversion process need to be defined

## Requirements

This template requires Python >= 3.7.

As well as typical scientific Python packages, dependencies include:

- [convnwb](https://github.com/JacobsSU/convnwb)
- [pynwb](https://github.com/NeurodataWithoutBorders/pynwb)

The full list of dependencies is listed in `requirements.txt`.

Note that extra dependencies may need to be added when using this template for any given task / dataset.

## Data Organization

This template doesn't assume any particular file structure or file type, however, files will need to be
organized into a consistent layout, and I/O procedures may need to be updated for particular file types.

## Repository Layout

This repository is set up in the following way:

- `conv/` contains custom code for processing and converting data
- `notebooks/` contains notebooks that demonstrate examples of data conversion
- `metadata/` contains config files that define metadata fields and task descriptions
- `scripts/` contains stand alone scripts to process data files
- `temp/` is a run folder for interim files when processing data

## Run Procedures

Data files can be processed by running the scripts available in the `scripts` folder.

For information on how this process proceeds, see the notebooks.

If anything needs to be updated, changes may be required to the stored metadata and/or
processing code. See the `Repository Layout` Section for information.
