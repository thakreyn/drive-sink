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
from datetime import datetime
from termcolor import colored
import configparser


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
        "root" : CURRENT_LOCATION
    }

    # User config details
    config['user'] = {}

    with open("./.sink/config/config.ini", "w") as configfile:
        config.write(configfile)


def read_config_file(section = "general", attr = "root"):
    """ Returns the mentioned attr from a given section 
        (Default: returns the init directory)    
    """

    config = configparser.ConfigParser()
    config.read("./.sink/config/config.ini")

    return config[section][attr]
    

def main_init_process():

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
        

        """
        Code for setting up User and the first scan of the directory
        """

        # ignore files
        with open("./.sink/ignore.txt", "w+") as file:
            pass

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

        print(colored("Folder has been successfully initialised at " + CURRENT_LOCATION, 'green'))


    else:
        print(colored("[Error] : A folder has already been initilised here !", 'red'))
        



