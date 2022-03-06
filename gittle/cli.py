import click

from gittle.init import init as cmd_init
from gittle.add import add as cmd_add


@click.group()
def cli():
    """Gittle."""


@cli.command()
def init():
    """Initialise a gittle repo."""
    cmd_init()


@cli.command()
def add():
    """Stage files for adding to a gittle repo."""
    cmd_add()
