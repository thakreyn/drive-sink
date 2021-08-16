import os
import click

import init as user_init
import scan as user_scan
import utility as user_utility


@click.command()
def init():
    ''' Main logic for Initialing the folder. Calls init.py '''
    user_init.main_init_process()


@click.command()
def status():
    """ Display status """
    print("status")
    print(user_init.read_config_file("general", "root"))


@click.command()
def scan():
    """ Scan and display status """
    if user_init.check_pre_init():
        user_scan.full_scan()
    else:
        pass   


# Definition of CLI group
@click.group()
def cli():
    pass

cli.add_command(status)
cli.add_command(scan)
cli.add_command(init)


if __name__ == '__main__':
    cli()