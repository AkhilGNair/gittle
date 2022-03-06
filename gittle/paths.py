from functools import lru_cache
from pathlib import Path
from typing import Dict

GITTLE = ".gittle"
STAGING_RECORD = ".stage"


@lru_cache(maxsize=None)
def get_repo_paths() -> Dict[str, Path]:
    cwd = Path.cwd()
    return {
        "root": cwd,
        "gittle": cwd / GITTLE,
        "store": cwd / GITTLE / "store",
        "head": cwd / GITTLE / "HEAD",
        "workspace": cwd / GITTLE / "workspace",
    }


def path_staging():
    paths = get_repo_paths()
    return paths["gittle"] / STAGING_RECORD


def store_empty():
    paths = get_repo_paths()
    return not bool(len(list(paths["store"].rglob("*"))))
