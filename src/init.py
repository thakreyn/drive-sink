""" 
    init.py:

    Responsible for setting up the directory for synchronisation and setting up 
    the user profile.
    
    - Checks the directory if already initialised.
    - Setups up directory structure
    - Asks user data
    - Sets up user Files and preferences
    - Confirms creation and prints help message

"""

import os
import shutil
from datetime import datetime
from termcolor import colored
import configparser

from . import scan as user_scan
from . import drive as user_drive


CURRENT_LOCATION = os.getcwd()


def check_pre_init():
    """ Checks if folder has been inititalised for sync and returns bool
        True -> Already init
        False -> Not init
     """

    filename = CURRENT_LOCATION + "\.sink"

    if os.path.exists(filename):
        return True
    
    return False


def generate_config_file():
    """ 
    Generates the initial config.ini file for the user
    File contains the following data :
        2 sections -> general, user    
    """ 

    config = configparser.ConfigParser()

    # General config details
    config['general'] = {
        "root" : CURRENT_LOCATION,
        "drive_status" : False,
        "populated" : False
    }

    # User config details
    config['user'] = {
        "folder_name" : CURRENT_LOCATION,
        "folder_id" : ""
    }

    with open("./.sink/config/config.ini", "w") as configfile:
        config.write(configfile)


# Also available in utility.py
def read_config_file(section = "general", attr = "root"):
    """ Returns the mentioned attr from a given section 
        (Default: returns the init directory)    
    """

    config = configparser.ConfigParser()
    config.read("./.sink/config/config.ini")

    return config[section][attr]


def edit_config_file(section, attr, new_attr):
    """ Edits the mentioned section and attr in the config.ini """

    edit = configparser.ConfigParser()
    edit.read(read_config_file() + "/.sink/config/config.ini")

    edit_section = edit[section]
    edit_section[attr] = new_attr

    with open( read_config_file() + "/.sink/config/config.ini", "w") as configfile:
        edit.write(configfile)
    

def main_init_process():
    """
        Main initialisation routine
        Init steps: 
            1. Establish '.sink' directory
            2. Create subfolders (log, config, meta)
            3. Generate config file
            4. Generate ignore file
            5. Generate log files (usage, commit)
            6. Complete first scan and write to metadata
            7. Establish the drive-sink directory in users folder
    """

    if not check_pre_init():
        print("Initialising at : " + CURRENT_LOCATION)

        directory = ".sink"


        path = os.path.join(CURRENT_LOCATION, directory)
        os.mkdir(path)

        subdirectories = ["log", "config", "meta"]

        # Create mentioned subdirectories
        for subdirectory in subdirectories:
            path = os.path.join(CURRENT_LOCATION + "/.sink" , subdirectory)
            os.mkdir(path)

        # Check if drive-sink is available in users directory, else -> initialise it (with name .drive-sink)

        user_folder_path = os.path.expanduser("~")
        user_folder_path = os.path.join(user_folder_path, ".drive-sink")

        if not os.path.exists(user_folder_path):
            os.mkdir(user_folder_path)
            

        # config file
        generate_config_file()
        
        # ignore files
        with open("./.sink/ignore.txt", "w+") as file:
            text = "!__pycache__\n!.sink\n!sink\ncredentials.json\ntoken.json"
            file.write(text)
            
        # usage log
        with open("./.sink/log/usage.log", "w+") as file:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_message = f"[{time}] : Initialised Folder at -> {CURRENT_LOCATION}"
            file.write(log_message)

        # commit log
        with open("./.sink/log/commit.log", "w+") as file:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_message = f"[{time}] : Initialised Folder at -> {CURRENT_LOCATION}"
            file.write(log_message)

        
        # Check if credentials already exist, then inform the user about the file being used
        # and give option to use local credentials file

        if os.path.exists(os.path.join(user_folder_path, 'credentials.json')):
            print(f"\nCredentials.json already found at global location {colored(user_folder_path, 'green')} using it by default.")

            print(f"""
            {colored("Folder has been successfully initialised at " + CURRENT_LOCATION, 'green')}
            Run command:
            
                '{colored("sink initdrive", 'green')}' to enable the drive and verify.

            (optional) If you want to use local credentials, please copy 'credentials.json' to '.sink/config' 
            and then run `sink initdrive`.
            If you don't have a credentials.json file, see documentation for instructions to generate one.
            If this directory was initialised by mistake, use 'sink clean' to cancel.
            """)

        else:
            print(f"""
            {colored("Folder has been successfully initialised at " + CURRENT_LOCATION, 'green')}
            {colored("No global 'credentials.json' found!", 'red')}
            Please copy 'credentials.json' to '{user_folder_path}' for global access or 
            to '.sink/config' if you want to use different local credentials. 
            Then run :

                '{colored("sink initdrive", 'green')}' to enable drive and verify.
                
            If you don't have a credentials.json file, see documentation for instructions to generate one.
            If this directory was initialised by mistake, use 'sink clean' to cancel.
            """)

       


    else:
        print(colored("[Error] : A folder has already been initilised here !", 'red'))
        

def clean_setup():
    """ 
        Completely deletes the sink directory with all config files and 
        option to delete the drive folder as well
    """

    if check_pre_init():
        location = read_config_file()
        dir = ".sink"
        path = os.path.join(location, dir)

        if input("Do you want to delete drive folder as well ? (y/n) : ").lower() == 'y':
            if read_config_file("general", "drive_status") == 'True':
                mydrive = user_drive.MyDrive()
                root_id = read_config_file("user", "folder_id")
                mydrive.delete_file(root_id)


        shutil.rmtree(path)
        print(colored("Successfully deleted and cleaned the setup",'green'))
    else:
        print("No directory found to clean!!")