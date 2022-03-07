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
    root = gittle.paths.root()
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
        changed = gittle.commit.find_files()
    else:
        changed = gittle.commit.detect_changes()

    if not changed:
        click.secho("No changes detected since last commit", fg="green")
        sys.exit(0)

    preselected = [_file in staged for _file in changed]

    new_stage = questionary.checkbox(
        "Which files do you want to stage?",
        choices=[
            questionary.Choice(_file, checked=check) for _file, check in zip(changed, preselected)
        ],
    ).ask()

    if new_stage is None:
        click.secho("Operation cancelled by user", fg="red")
        sys.exit(1)

    if set(staged).symmetric_difference(new_stage):
        gittle.stage.write(new_stage)
        click.secho("Updated staging area", fg="green")
    else:
        click.secho("Staging area unchanged", fg="yellow")


@cli.command()
def commit():
    staged = gittle.stage.read()

    if not staged:
        click.secho("Nothing to commit!", fg="yellow")
        sys.exit(0)

    commit = gittle.commit.take_snapshot()

    click.secho(
        f"Wrote the snapshot (commit) called '{commit}' to the gittle store",
        fg="green",
    )


@cli.command()
@click.argument("commit")
def cat_object(commit):
    blob = gittle.commit.read_blob(commit)

    if "file" in blob:
        click.secho("File:", fg="green")
        click.echo(blob["file"])
        click.echo("")

        click.secho("Content:", fg="green")
        click.echo(blob["content"])

    if "parents" in blob:
        click.secho("Parents:", fg="green")
        for parent in blob["parents"]:
            click.echo(f" - {parent}")
        else:
            click.echo("Root commit")
        click.echo("")

        click.secho("Hashes:", fg="green")
        for hash in blob["content"]:
            click.echo(f" - {hash}")
