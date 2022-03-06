from pathlib import Path

from gittle.paths import branches, head


def current_branch():
    return head().read_text()


def current_commit():
    return (branches() / current_branch()).read_text()


def update(commit: str):
    Path(branches()).mkdir(parents=True, exist_ok=True)
    branch_ref = branches() / current_branch()
    branch_ref.write_text(commit)
