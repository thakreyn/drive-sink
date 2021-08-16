"""
    utility.py:
    
    Contains the following utility files :
    1. Log 
    2. 
"""

import os
from datetime import datetime

import init as user_init


def log(message , file = "usage.log"):
    """ Log Message -> message and file options : [usage.log, commit.log] """

    curr_dir = user_init.read_config_file()

    path = curr_dir + "/.sink/log/" + file

    with open(path , "a") as file:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_message = f"\n[{time}] : {message}"
            file.write(log_message)

