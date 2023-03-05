"""
This file contains the paths of files and directories from project's root path.
"""

import os

dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir_path)


class Paths:
    PROjECT_PATH = os.path.join(dir_path, '')
    CONFIG_FILE_PATH = os.path.join(dir_path, '.config.yaml')
