"""Utility & helper functions."""

import os
import re
from itertools import product
from pandas import DataFrame
from typing import List
from typing import Union
# Link in functions from convnwb
from convnwb.utils.tools import incrementer, get_current_date
from convnwb.utils.convert import convert_time_to_date
from convnwb.utils.validate import validate_nwb
from convnwb.utils.log import print_status
from convnwb.utils.run import catch_error

import os
import re
from itertools import product
from pandas import DataFrame


def group_files(
        directories: Union[str, List[str]],
        group_reg_pattern: str = r'.*?(?=\_\d{1}|\.ncs)',
        suffix_reg_pattern: str = r'(?<=\_)\d*',
        order_by_create_time: bool = False,
        ignore_files_with_size_below: int = 16384
):
    """Group files based on their name pattern.

    This function lists files in the directory that matches specific
    patterns and organizes them into a cell array. Files in the same group
    are in the same row. e.g.
       'dir/GA1-RA1.ncs', 'dir/GA1-RA1_0002.ncs', 'dir/GA1-RA1_0003.ncs'
       'dir/GA1-RA2.ncs', 'dir/GA1-RA2_0002.ncs', 'dir/GA1-RA2_0003.ncs'

    Arguments:
        directories - string, List[str]. A list of directories in which the
            files will be grouped based on their name pattern. Files in different
            directories will be concatenated by column.
        group_reg_pattern - string. A regular expression used to determine the
            group name of files in the directory. File names are decomposed to
            `[group]_[suffix].[extension]`. Files with the same group will be put in
            the same row in the returned cell array.
        suffix_reg_pattern - string. A regular expression used to determine the
            suffix of files in the directory. File names are decomposed to
            `[group]_[suffix].[extension]`.
        order_by_create_time - boolean. If true, order files in the same group
            (row) by create date, otherwise, order by suffix. Empty suffix will be
            first. This only works within the directory.
        ignore_files_with_size_below - int. File size in bytes. Files with a smaller
            size than this will be ignored.

    Outputs:
        groups - List [m]. group pattern extracted from file names.
        file_names - pd.DataFrame [m, n]. file names grouped in rows.
        group_file_names - pd.DataFrame [m, n + 1]. data table combines groups and
            file_names, this can be saved as a .csv file to check the files combined.
        event_file_names - List [n]. '.env' files to be combined. If no event
            files found in directories{i}, it will be empty.
    """

    def get_file_names(directory: str, file_ext: str) -> List[str]:
        filenames = [f for f in os.listdir(directory) if
                     os.path.isfile(os.path.join(directory, f)) and f.endswith(file_ext)]
        if ignore_files_with_size_below is not None:
            filenames = [f for f in filenames if
                         os.path.getsize(os.path.join(directory, f)) > ignore_files_with_size_below]
        return filenames

    group_file_names_list = []
    event_file_names = []

    for directory in directories:
        # .ncs files:
        filenames = get_file_names(directory, '.ncs')
        file_group = list(set([re.search(group_reg_pattern, filename).group() for filename in filenames]))
        file_suffix = list(
            set([re.search(suffix_reg_pattern, filename).group() if re.search(suffix_reg_pattern, filename) else '' for
                 filename in filenames]))

        file_suffix = ['_' + suffix if suffix else '' for suffix in file_suffix]

        group_file_names = []
        for suffix, group in product(file_suffix, file_group):
            filename = os.path.join(directory, group + suffix + '.ncs')
            if os.path.isfile(filename):
                group_file_names.append(filename)

        if order_by_create_time and len(file_suffix) > 1:
            print("group_files: order files by create time.")
            raise NotImplementedError()
        elif len(file_suffix) > 1:
            print("group_files: order files by file name. Make sure the order is correct by checking groupFileNames!")
            group_file_names.sort()

        group_file_names_list.append(DataFrame({'file_group': file_group, 'file_names': group_file_names}))

        # nev files:
        nev_filenames = get_file_names(directory, '.nev')
        if len(nev_filenames) > 1 and order_by_create_time:
            print("group_files: order .nev files by start time stamp:")
            raise NotImplementedError()
        elif len(event_file_names) > 1:
            print()

        event_file_names.extend([os.path.join(directory, nev) for nev in nev_filenames])

    groups = [group for df in group_file_names_list for group in df['file_group']]
    file_names = [list(df.loc[df['file_group'] == group, 'file_names']) for df in group_file_names_list for group in
                  df['file_group']]
    group_file_names = DataFrame({'file_group': groups, 'file_names': file_names})

    return groups, file_names, group_file_names, event_file_names
