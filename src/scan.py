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

from . import init as user_init
from . import utility as user_utility
from . import drive as user_drive


class Folder:
    def __init__(self, name, root, parent_id, folder_id):
        self.name = name
        self.root = root
        self.parent_id = parent_id
        self.folder_id = folder_id

    def __str__(self):
        return f"Folder data : {self.name} : {self.root} : {self.parent_id} : {self.folder_id}"


class File:
    def __init__(self, name, root, parent_id, file_id, file_hash):
        self.name = name
        self.root = root
        self.parent_id = parent_id
        self.file_id = file_id
        self.hash = file_hash

    def __str__(self):
        return f"File data : {self.name} : {self.root} : {self.parent_id} : {self.file_id} : {self.hash}"


def hashing_function(filename):
    """ Takes in complete file path as input and returns MD5 hash of contents """

    md5_hash = hashlib.md5()

    with open(filename, "rb") as f:
        content = f.read()
        md5_hash.update(content)

    return md5_hash.hexdigest()


def ignore_list(curr_dir, mode = 0):
    """ 
        Returns a list of only filenames (without root and with extensions) to be ignored 
        Mode = 0 -> returns files
        Mode = 1 -> returns directories
    """

    path = curr_dir + "/.sink/ignore.txt"

    with open(path, "r") as ignorefile:
        ignore_files = ignorefile.read().split("\n")
    ignore_directories = []


    i = 0
    while i < len(ignore_files):

        entry = ignore_files[i]
        if not entry:
            i += 1
            continue

        if entry[0] == '!':
            ignore_directories.append(entry[1:])
            ignore_files.pop(i)
        else:
            i += 1

    if mode == 0:
        return ignore_files
    else:
        return ignore_directories
    

def write_metadata(metadata, mode = 0):
    """ 
        Writes the filedict data to filesdata in metadata. Can take dict as input or default
        Mode : 0 -> filesdata.pickle
               1 -> foldersdata.pickle
     """

    curr_dir = user_init.read_config_file("general", "root")

    if mode == 0:
        path = curr_dir + "/.sink/meta/filesdata.pickle"
    else:
        path = curr_dir + "/.sink/meta/foldersdata.pickle"


    with open(path , "wb") as file:
        pickle.dump(metadata, file)

    user_utility.log(f"Metadata written to file mode : {mode}")


def read_metadata(mode = 0):
    """ 
        Loads the datafile from .sink/meta/filesdata.pickle and returns dict 
        Mode : 0 -> filesdata.pickle
               1 -> foldersdata.pickle
    """

    curr_dir = user_init.read_config_file("general", "root")

    if mode == 0:
        path = curr_dir + "/.sink/meta/filesdata.pickle"
    else:
        path = curr_dir + "/.sink/meta/foldersdata.pickle"

    with open(path, "rb") as file:
        prefiledict = pickle.load(file)

    return prefiledict


def make_folder_changes():
    """ Take data from scan_folder_changes and then commit them to drive """

    mydrive = user_drive.MyDrive()

    folder_data = read_metadata(1)
    new_folders , deleted_folders = scan_folder_changes()

    curr_dir = user_init.read_config_file()
    curr_dir_id = user_init.read_config_file("user", "folder_id")

    # Adding folders

    

    for k , v in new_folders.items():
        # Check if folder root is drive root v[0] = root and v[1] = dir
        if v[0] == curr_dir:
            new_folder_id = mydrive.create_folder(v[1], curr_dir_id)
            folder_data[k] = Folder(v[1], v[0], curr_dir_id, new_folder_id)
        else:
            try:
                new_folder_id = mydrive.create_folder(v[1], folder_data[v[0]].folder_id)
                folder_data[k] = Folder(v[1], v[0], folder_data[v[0]].folder_id, new_folder_id)
            except:
                pass
        
        write_metadata(folder_data, 1)

    ## Deletion logic

    for k, v in deleted_folders.items():
        mydrive.delete_file(v.folder_id)
        folder_data.pop(k)
        write_metadata(folder_data, 1)

    user_utility.log(f"{len(new_folders)} folders added , {len(deleted_folders)} folders deleted")
    write_metadata(folder_data, 1)


def if_ignored(root, dir, ignore_list):
    """ Input -> Complete root path
        Output-> 
     """

    curr_dir = user_utility.read_config_file()

    root = root.replace(curr_dir, '')
    
    if root != '':
        root = root[1:].split(root[0])
        
        for folder in root:
            if folder in ignore_list:
                return True
    

    return False
    

def scan_folder_changes():
    """
        Scans for any new folders created or deleted and
        returns a tuple of dicts having new folders and deleted folders 
    """
    try:
        print("Folders : ")

        curr_dir = user_init.read_config_file()

        ignored = ignore_list(curr_dir , 1 )

        folder_data = read_metadata(1)

        # Entries in the form of 'root + dir : (root, dir)'
        new_folders = dict()

        for root, dirs, files in os.walk(curr_dir):
            for dir in dirs:
                if dir in ignored or if_ignored(root, dir, ignored):
                    continue
                else:
                    if os.path.join(root, dir) not in folder_data.keys():
                        new_folders[os.path.join(root, dir)] = (root, dir)


        # Deleted

        deleted_folders = dict()

        for folder, data in folder_data.items():
            if not (os.path.exists(folder)):
                deleted_folders[folder] = data

        # Logging

        if len(new_folders) == 0:
            print("No new folders added!")
        else:
            print(f"{len(new_folders)} new folder/folders added : ")
            for key in new_folders.keys():
                print(colored("\t" + key, 'green'))

        if len(deleted_folders) == 0:
            print("No folders were deleted!")
        else:
            print(f"{len(deleted_folders)} folder/folders were deleted : ")
            for key in deleted_folders.keys():
                print(colored("\t" + key, 'red'))

        return (new_folders, deleted_folders)

    except:
        user_utility.print_error("There is some problem with the installation! Reinstall to continue")
        exit(1)


def scan_file_changes():
    """
        Returns the data of changed files 
        (added, deleted, updated)

        added -> key : (root, dir)
        deleted -> path : object
        updated -> path : object
    """

    print("Files : ")

    curr_dir = user_init.read_config_file()
    curr_dir_id = user_init.read_config_file("user", "folder_id")

    file_data = read_metadata(0)
    folder_data = read_metadata(1)

    ignored = ignore_list(curr_dir)


    newfiles = dict()

    for root, dirs, files in os.walk(curr_dir):
        for file in files:
            if file in ignored:
                continue
            else:
                if os.path.join(root, file) not in file_data.keys():
                    if root in folder_data:
                        newfiles[os.path.join(root, file)] = (root, file)
                    if root == curr_dir:
                        newfiles[os.path.join(root, file)] = (root, file)

    # print(newfiles)

    deleted_files = dict()
    
    for file, data in file_data.items():
        if not (os.path.exists(file)):
            deleted_files[file] = data

    # print(deleted_files)

    updated_files = dict()

    for file, data in file_data.items():
        if os.path.exists(file):
            if hashing_function(file) != data.hash:
                updated_files[file] = data
                updated_files[file].hash = hashing_function(file)

    # print(updated_files)

    if len(newfiles) == 0:
        print("No new files added!")
    else:
        print(f"{len(newfiles)} new file/files added : ")
        for key in newfiles.keys():
            print(colored("\t" + key, 'green'))

    if len(deleted_files) == 0:
        print("No files were deleted!")
    else:
        print(f"{len(deleted_files)} file/files were deleted : ")
        for key in deleted_files.keys():
            print(colored("\t" + key, 'red'))

    if len(updated_files) == 0:
        print("No files were updated!")
    else:
        print(f"{len(updated_files)} file/files were updated: ")
        for key in updated_files.keys():
            print(colored("\t" + key, 'green'))


    return (newfiles, deleted_files, updated_files)


def make_file_changes():
    """ Commit the scanned changes to the drive and local machines """

    mydrive = user_drive.MyDrive()
    curr_dir = user_init.read_config_file()
    curr_dir_id = user_init.read_config_file("user", "folder_id")

    new_files , deleted_files , updated_files = scan_file_changes()

    file_data = read_metadata(0)
    folder_data = read_metadata(1)

    # Addition

    for file, value in new_files.items():
        if value[0] == curr_dir:
            new_file_id = mydrive.upload_file(value[1], value[0], curr_dir_id)
            new_file_hash = hashing_function(file)
            file_data[file] = File(value[1], value[0], curr_dir_id,new_file_id, new_file_hash)
        else:
            parent_id = folder_data[value[0]].folder_id
            new_file_id = mydrive.upload_file(value[1], value[0], parent_id)
            new_file_hash = hashing_function(file)
            file_data[file] = File(value[1], value[0], parent_id, new_file_id, new_file_hash)
        
        write_metadata(file_data, 0)
        print(file_data[file])

    # Deletion

    for file, data in deleted_files.items():
        mydrive.delete_file(data.file_id)
        file_data.pop(file)
        write_metadata(file_data, 0)

    # Updation

    for file, data in updated_files.items():
        mydrive.update_file(data.name, data.root, data.file_id)
        print(f"{file} : Updated!")


        file_data[file] = data
        write_metadata(file_data, 0)

    user_utility.log(f"{len(new_files)} files added , {len(deleted_files)} files deleted and {len(updated_files)} files were updated")
    write_metadata(file_data, 0)


def init_folder_structure():
    """ Initializes the folder structure and generates the folder data

        Folder data format :
            name, root, parent_id, folder_id

     """

    curr_dir = user_init.read_config_file()
    curr_dir_id = user_init.read_config_file("user", "folder_id")

    ignored = ignore_list(curr_dir , 1 )
    print(ignored)
    mydrive = user_drive.MyDrive()

    folders = dict()

    for root, dirs, files in os.walk(curr_dir):
        for dir in dirs:
            if dir in ignored:
                continue
            else:
                if root == curr_dir:
                    new_folder_id = mydrive.create_folder(dir, curr_dir_id)
                    folders[os.path.join(root, dir)] = Folder(dir, root, curr_dir_id, new_folder_id)
                else:
                    if root in folders:
                        new_folder_id = mydrive.create_folder(dir, folders[root].folder_id)
                        folders[os.path.join(root,dir)] = Folder(dir, root, folders[root].folder_id, new_folder_id)

    write_metadata(folders, 1)

    user_utility.log("Folder structure initialised properly!")
    init_file_structure() 



def init_file_structure():
    """ Initializes the files inside the folders

        File data format: 
            name, root, parent_id, folder_id
     """

    curr_dir = user_init.read_config_file()
    curr_dir_id = user_init.read_config_file("user", "folder_id")

    folder_data = read_metadata(1)

    ignored = ignore_list(curr_dir)
    mydrive  = user_drive.MyDrive()

    filesdict = dict()

    for root, dirs, files in os.walk(curr_dir):
        for file in files:
            if file in ignored:
                continue
            else:
                if root == curr_dir:
                    new_file_id = mydrive.upload_file(file, root, curr_dir_id)
                    new_file_hash = hashing_function(os.path.join(root, file))
                    filesdict[os.path.join(root, file)] = File(file, root, curr_dir_id, new_file_id , new_file_hash)
                else:
                    if root in folder_data:
                        parent_id = folder_data[root].folder_id
                        new_file_id = mydrive.upload_file(file, root, parent_id)
                        new_file_hash = hashing_function(os.path.join(root, file))
                        filesdict[os.path.join(root, file)] = File(file, root, parent_id, new_file_id, new_file_hash)


    write_metadata(filesdict, 0)
    user_utility.edit_config_file("general", "populated", "True")
    user_utility.log("File structure initialised properly!")
    print("File structure initialised properly!")

