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
    stage = gittle.paths.path_staging()
    staged = gittle.add.read_stage() if stage.exists() else []

    if gittle.paths.store_empty():
        # Return all files
        changed = gittle.add.find_files()
        preselected = [_file in staged for _file in changed]

        new_stage = questionary.checkbox(
            "Which files do you want to stage?",
            choices=[
                questionary.Choice(_file, checked=check)
                for _file, check in zip(changed, preselected)
            ],
        ).ask()

    else:
        # Reconstruct the last snapshot repo state
        # Diff the current state to the last commit
        click.secho("Gittle 'add' with a non-empty store not implemented", fg="red")
        sys.exit(1)

    if set(staged).symmetric_difference(new_stage):
        gittle.add.write_staging(new_stage)
        click.secho("Updated staging area", fg="green")


@cli.command()
def commit():
    n, blob_name = gittle.commit.create_blob()

    if not n:
        click.secho("No file staged to commit!", fg="red")
        sys.exit(1)

    click.secho(
        f"Wrote a blob called '{blob_name}' with '{n}' files to the gittle store",
        fg="green",
    )
