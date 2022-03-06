import sys

import click
import questionary

import gittle


@click.group()
def cli():
    """Gittle."""


@cli.command()
def init():
    """Initialise a gittle repo."""
    paths = gittle.paths.get_repo_paths()
    root = paths["root"]
    exists = gittle.init.create_repo()
    if not exists:
        click.secho(f"Creating gittle repo at '{root}'", fg="green")
    else:
        click.secho(f"Gittle repo already exists at '{root}'", fg="yellow")


@cli.command()
def add():
    """Stage files for adding to a gittle repo."""
    stage = gittle.paths.staging()
    staged = gittle.stage.read() if stage.exists() else []

    if gittle.paths.store_empty():
        # Return all files
        changed = gittle.add.find_files()
    else:
        changed = gittle.add.detect_changes()

    preselected = [_file in staged for _file in changed]

    new_stage = questionary.checkbox(
        "Which files do you want to stage?",
        choices=[
            questionary.Choice(_file, checked=check) for _file, check in zip(changed, preselected)
        ],
    ).ask()

    if set(staged).symmetric_difference(new_stage):
        gittle.add.write_staging(new_stage)
        click.secho("Updated staging area", fg="green")


@cli.command()
def commit():
    commit = gittle.commit.take_snapshot()

    click.secho(
        f"Wrote the snapshot (commit) called '{commit}' to the gittle store",
        fg="green",
    )
