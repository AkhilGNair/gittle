from pathlib import Path
from glob import glob

from gittle.paths import get_paths, GITTLE


def store_empty():
    paths = get_paths()
    return not bool(len(list(paths["store"].rglob("*"))))


def find_files():
    include = glob("*") + glob(".*")
    exclude = glob(f"{GITTLE}/*") + [GITTLE]
    return set(include).difference(exclude)


def add():
    if store_empty():
        # Return all files
        print(find_files())
    else:
        # Check the head file
        # Reconstruct the last commit
        # Diff the current state to the last commit
        pass
