"""
    utility.py:
    
    Contains the following utility files :
    1. Log 
    2. 
"""

import os
from datetime import datetime
import configparser
from termcolor import colored

from . import init as user_init


def log(message , file = "usage.log"):
    """ Log Message -> message and file options : [usage.log, commit.log] """

    curr_dir = user_init.read_config_file()

    path = curr_dir + "/.sink/log/" + file

    with open(path , "a") as file:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_message = f"\n[{time}] : {message}"
            file.write(log_message)


def read_log(length, file = "commit.log"):
    """
        Returns a list of 'length' log messages from the file
    """

    curr_dir = user_init.read_config_file()

    path = curr_dir + "/.sink/log/" + file

    with open(path, 'r') as file:
        data = file.read().split('\n')

    data = data[::-1]

    if len(data) < length:
        return data
    else:
        return data[:length]



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
    

def print_error(message):
    """
        Prints red coloured error messsage to the terminal and logs it to the usage.log
    """
    print(colored(f"[Error] : {message}", 'red'))

    
def check_drive_init():
    """ Checks if the drive data is initialised
        True -> Initialised
        False -> Not
     """

    return (read_config_file("general", "drive_status"))