import os
import click

import init as user_init
import scan as user_scan
import utility as user_utility
import drive as user_drive


@click.command()
def init():
    ''' Initializes the local directory structure '''
    user_init.main_init_process()


@click.command()
def status():
    """ Display status """
    user_scan.updates(user_scan.read_metadata(), user_scan.initial_scan(user_init.read_config_file()))


@click.command()
def scan():
    """ Scan and display changes in the directory """
    if user_init.check_pre_init() and user_utility.check_drive_init():
        user_scan.scan_folder_changes()
        user_scan.scan_file_changes()
        # user_scan.ignore_list(user_utility.read_config_file())
    else:
        pass   


@click.command()
def initdrive():
    """ Run this command after placing credentials.json in .sink/config to verify and authenticate drive """
    if user_init.check_pre_init():
        if user_drive.init_drive_files():
            user_scan.init_folder_structure()


@click.command()
def clean():
    """ Clean the sink initialisation and delete all config files """
    user_init.clean_setup()


@click.command()
def sync():
    """ Synchronizes the changes with the drive """

    if user_init.check_pre_init() and user_utility.check_drive_init():
        user_scan.make_folder_changes()
        user_scan.make_file_changes()



@click.command()
def test():
    """ Test Commands """
    # user_scan.make_folder_changes()
    # user_scan.scan_file_changes()
    user_scan.make_folder_changes()
    user_scan.make_file_changes()
    # user_scan.walk()


# Definition of CLI group
@click.group()
def cli():
    pass

cli.add_command(sync)
cli.add_command(scan)
cli.add_command(init)
cli.add_command(initdrive)
cli.add_command(clean)
cli.add_command(test)

# Changed


if __name__ == '__main__':
    cli()   