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
import pickle

import init as user_init
import utility as user_utility


def hashing_function(filename):
    """ Takes in complete file path as input and returns MD5 hash of contents """

    md5_hash = hashlib.md5()

    with open(filename, "rb") as f:
        content = f.read()
        md5_hash.update(content)

    return md5_hash.hexdigest()


def initial_scan(curr_dir):
    """ Completely scans the directory and returns dict of files and their hash """

    filedict = dict()
    # curr_dir = user_init.read_config_file("general", "root")

    ignored = ignore_list(curr_dir)

    for root, dirs, files in os.walk(curr_dir):
        for filename in files:
            if filename in ignored:
                continue
            else:
                filedict[os.path.join(root, filename)] = hashing_function(os.path.join(root, filename))


    return filedict


def ignore_list(curr_dir):
    """ Returns a list of only filenames (without root and with extensions) to be ignored """

    path = curr_dir + "/.sink/ignore.txt"

    with open(path, "r") as ignorefile:
        ignore_text = ignorefile.read().split("\n")

    return ignore_text

    

def write_metadata(metadata):
    """ Writes the filedict data to filesdata in metadata. Can take dict as input or default """

    curr_dir = user_init.read_config_file("general", "root")
    path = curr_dir + "/.sink/meta/filesdata.pickle"

    with open(path , "wb") as file:
        pickle.dump(metadata, file)

    user_utility.log("Scan completed and metadata written")


def read_metadata():
    """ Loads the datafile from .sink/meta/filesdata.pickle and returns dict"""

    curr_dir = user_init.read_config_file("general", "root")
    path = curr_dir + "/.sink/meta/filesdata.pickle"

    with open(path, "rb") as file:
        prefiledict = pickle.load(file)

    return prefiledict


def updates(prefiledict, filedict):
    """ """

    added = [x for x in filedict.keys() if x not in prefiledict.keys()]
    deleted = [x for x in prefiledict.keys() if x not in filedict.keys()]

    updated = list()

    for file in filedict.keys():
        if file in prefiledict.keys():
            if filedict[file] != prefiledict[file]:
                updated.append(file)

    print(f"{len(added)} New Files Identified : ")
    for file in added:
        print("\t" + colored(file, 'green'))

    print(f"{len(updated)} Files Updated : ")
    for file in updated:
        print("\t" + colored(file, 'green'))

    print(f"{len(deleted)} Files Deleted : ")
    for file in deleted:
        print("\t" + colored(file, 'red'))


def test_scan():

    curr_dir = user_init.read_config_file() 

    for root, dirs, files in os.walk(curr_dir):
        for file in dirs:
            print(file, root)
