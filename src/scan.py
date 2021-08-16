"""
    scan.py:

    Responsible for retrieving the exisitng metadata, scanning the current
    files and identify updates/differences (generating update, added and delted lists)

    - Retrieve previous data
    - Scan current files
    - Check Added
    - Check Deleted
    - Check Updated
    - Store new metadata

    (Output returned in the from of lists with complete file_paths as elements)
    (Return Summary of changes)
    (Metadata is stored in the form of dict with key: value as path : hash)
"""

import os
import hashlib
from termcolor import colored

import init as user_init


EXISTING_DATA = dict()


def hashing_function(filename):
    """ Takes in complete file path as input and returns MD5 hash of contents """

    md5_hash = hashlib.md5()

    with open(filename, "rb") as f:
        content = f.read()
        md5_hash.update(content)

    return md5_hash.hexdigest()


def load_data():
    """ Loads the datafile from .sink/meta/ """

    with open(".\.sink\meta\datafile", "rb"):
        pass


def write_data(final_dict):
    """ Writes the datafile to .sink/meta/datafile.pickle """


def full_scan():
    """ Completely scans the directory and gives summary """

    filedict = dict()
    curr_dir = user_init.read_config_file("general", "root")

    for root, dirs, files in os.walk(curr_dir):
        for filename in files:
            filedict[os.path.join(root, filename)] = hashing_function(os.path.join(root, filename))

    prefiledict = dict()

    added = [x for x in filedict.keys() if x not in prefiledict.keys()]

    print("New Files Identified : ")
    
    for file in added:
        print("\t" + colored(file, 'green'))
    




