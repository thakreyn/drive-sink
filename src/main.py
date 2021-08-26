#!d:\projects\sink\env\scripts\python.exe

import os
import click

from . import init as user_init
from . import scan as user_scan
from . import utility as user_utility
from . import drive as user_drive


@click.command()
def init():
    ''' Initializes the local directory structure '''
    user_init.main_init_process()


@click.command()
def status():
    """ Display status """
    # user_scan.updates(user_scan.read_metadata(), user_scan.initial_scan(user_init.read_config_file()))

    if user_init.check_pre_init():
        print(f"""
        Root Folder : {user_utility.read_config_file()}
        Drive Status : {user_utility.read_config_file("general", "drive_status")}
        Drive Folder Name : {user_utility.read_config_file("user", "folder_name")}
        Drive Folder id : {user_utility.read_config_file("user", "folder_id")}
        """)

    else:
        user_utility.print_error("Sink folder not found! Initialise folder using 'sink init'")


@click.command()
def initdrive():
    """ Run this command after placing credentials.json in .sink/config to verify and authenticate drive """

    if user_init.check_pre_init():
        if user_drive.init_drive_files():
            user_scan.init_folder_structure()

    else:
        user_utility.print_error("Sink folder not Found! Initialise folder first or reset your configuration!") 


@click.command()
def clean():
    """ Clean the sink initialisation and delete all config files """
    user_init.clean_setup()


@click.command()
def scan():
    """ Scan and display changes in the directory """
    
    if user_init.check_pre_init() and user_utility.check_drive_init() == "True":
        user_scan.scan_folder_changes()
        user_scan.scan_file_changes()
        # user_scan.ignore_list(user_utility.read_config_file())
    else:
        user_utility.print_error("Sink folder not Found! Initialise folder first or reset your configuration!")   


@click.command()
@click.option('-m', '--message', help="Enter the commit message for commit log (in quotes)")
def sync(message):
    """ Synchronizes the changes with the drive """

    if user_init.check_pre_init() and user_utility.check_drive_init() == 'True':
        user_scan.make_folder_changes()
        user_scan.make_file_changes()

        if message:
            user_utility.log(message, "commit.log")

    else:
        user_utility.print_error("Sink folder not Found! Initialise folder first or reset your configuration!")


@click.command()
@click.option('-m', '--message', help="Enter the commit message for commit log (in quotes)")
def test(message):

    if message:
        print(message)
    """ Test Commands """


@click.command()
@click.option('-l', '--length', default=5, type=int, help="Number of lines to print from log")
@click.option('-f', '--file', default="commit.log", type=str, help="Choose from usage.log and commit.log")
def log(length, file):
    """ Prints the user commit log """

    if user_init.check_pre_init() and user_utility.check_drive_init() == 'True':
        
        data = user_utility.read_log(length, file)

        for log in data:
            print(log)


    else:
        user_utility.print_error("Sink folder not Found! Initialise folder first or reset your configuration!")



# Definition of CLI group
@click.group()
def cli():
    pass

cli.add_command(sync)
cli.add_command(scan)
cli.add_command(init)
cli.add_command(initdrive)
cli.add_command(clean)
cli.add_command(log)
cli.add_command(test)
cli.add_command(status)


if __name__ == '__main__':
    cli()   