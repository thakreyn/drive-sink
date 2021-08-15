import os
import click


@click.command()
def init():
    ''' Main logic for Initialing the folder. Calls init.py '''
    click.echo("init. . .")


# Definition of CLI group
@click.group()
def cli():
    pass

cli.add_command(init)


if __name__ == '__main__':
    cli()