# ConvertTEMPLATE

Template structure for converting data to NWB format.

[![Template](https://img.shields.io/badge/template-HSUPipeline/ConvertTEMPLATE-yellow.svg)](https://github.com/HSUPipeline/ConvertTEMPLATE)
[![Sort](https://img.shields.io/badge/analysis-SortTEMPLATE-lightgrey)](https://github.com/HSUPipeline/SortTEMPLATE)
[![Analysis](https://img.shields.io/badge/analysis-AnalyzeTEMPLATE-lightgrey)](https://github.com/HSUPipeline/AnalyzeTEMPLATE)

## TEMPLATE DESCRIPTION

This repository provides a template for managing and converting data files into the
[neurodata without borders](https://www.nwb.org/) format.

This template follows the general purpose
[ProjectTemplate](https://github.com/structuredscience/ProjectTemplate)
layout from
[StructuredScience](https://github.com/structuredscience/).

For information on how to use this template in a project, see the
[HSUPipeline Guide](https://github.com/HSUPipeline/Overview/blob/main/Guide.md).

Note: if copying this template for use, this section can be removed.

## Overview

**Provide an overview of the analysis project here, for example:**

This repository is for managing and converting data files for the XX task,
processing and converting the data into the
[neurodata without borders](https://www.nwb.org/) format.

This conversion follows the [ConvertTEMPLATE](https://github.com/HSUPipeline/ConvertTEMPLATE).

## Requirements

**Fill in any extra requirements here.**

This repository requires Python >= 3.7.

As well as typical scientific Python packages, dependencies include:

- [pynwb](https://github.com/NeurodataWithoutBorders/pynwb)
- [convnwb](https://github.com/HSUPipeline/convnwb)

The full list of dependencies is listed in `requirements.txt`.

## Repository Layout

This repository is set up in the following way:

- `conv/` inherits from `convnwb` and contains any extra custom code for converting data
- `notebooks/` contains notebooks that demonstrate examples of data conversion
- `metadata/` contains config files that define metadata fields and task descriptions
- `scripts/` contains stand alone scripts to process data files

## Run Procedures

Data files can be processed by running the scripts available in the `scripts` folder.

The procedures are also detailed through the `notebooks`.

For a detailed description of how this approach works, and instructions on making
updates, see the [ConvertTEMPLATE](https://github.com/HSUPipeline/ConvertTEMPLATE).
