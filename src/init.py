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

import scan as user_scan
import drive as user_drive


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
            6. Copmlete first scan and write to metadata

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

        
        # Creating files : 

        # config file
        generate_config_file()
        
        # ignore files
        with open("./.sink/ignore.txt", "w+") as file:
            text = "!__pycache__\n!.sink\n!sink"
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

        """
        Code for setting up User and the first scan of the directory
        """
        # First Scan 
        # user_scan.write_metadata(user_scan.initial_scan(read_config_file()))

        print(colored("Folder has been successfully initialised at " + CURRENT_LOCATION, 'green'))
        print("Please copy 'credentials.json' to '.sink/config' and then run : '" , colored("python main.py initdrive", 'green') , "' to enable drive and verify. ")


    else:
        print(colored("[Error] : A folder has already been initilised here !", 'red'))
        


# To delete the drive folder as well !!!
def clean_setup():
    """ Completely deletes the sink directory with all config files """

    if check_pre_init():
        location = read_config_file()
        dir = ".sink"
        path = os.path.join(location, dir)

        if input("Do you want to delete drive folder as well ? (y/n)").lower() == 'y':
            mydrive = user_drive.MyDrive()
            root_id = read_config_file("user", "folder_id")
            mydrive.delete_file(root_id)


        shutil.rmtree(path)
        print(colored("Successfully deleted and cleaned the setup",'green'))
    else:
        print("No directory found to clean!!")