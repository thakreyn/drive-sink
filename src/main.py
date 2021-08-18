import os
import click

import init as user_init
import scan as user_scan
import utility as user_utility
import drive as user_drive


@click.command()
def init():
    ''' Main logic for Initialing the folder. Calls init.py '''
    user_init.main_init_process()


@click.command()
def status():
    """ Display status """
    user_scan.updates(user_scan.read_metadata(), user_scan.initial_scan(user_init.read_config_file()))


@click.command()
def scan():
    """ Scan and display status """
    if user_init.check_pre_init():
        user_scan.full_scan()
    else:
        pass   


@click.command()
def initdrive():
    """ Run this command after placing credentials.json in .sink/config to verify and authenticate drive """
    user_drive.init_drive_files()


@click.command()
def clean():
    """ Clean the sink initialisation and delete all config files """
    user_init.clean_setup()


# Definition of CLI group
@click.group()
def cli():
    pass


@click.command()
def test():
    """ Test Commands """
    user_scan.test_scan()

cli.add_command(status)
cli.add_command(scan)
cli.add_command(init)
cli.add_command(initdrive)
cli.add_command(clean)
cli.add_command(test)


if __name__ == '__main__':
    cli()   