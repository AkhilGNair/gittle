from functools import lru_cache
from pathlib import Path
from typing import Dict

GITTLE = ".gittle"
REFERENCES = "references"


@lru_cache(maxsize=None)
def get_repo_paths() -> Dict[str, Path]:
    cwd = Path.cwd()
    return {
        "root": cwd,
        "gittle": cwd / GITTLE,
        "store": cwd / GITTLE / "store",
        "head": cwd / GITTLE / "HEAD",
        "workspace": cwd / GITTLE / "workspace",
        "staging": cwd / GITTLE / ".stage",
        "references": cwd / GITTLE / REFERENCES,
        "branches": cwd / GITTLE / REFERENCES / "branches",
    }


def root() -> Path:
    paths = get_repo_paths()
    return paths["root"]


def store() -> Path:
    paths = get_repo_paths()
    return paths["store"]


def staging() -> Path:
    paths = get_repo_paths()
    return paths["staging"]


def head() -> Path:
    paths = get_repo_paths()
    return paths["head"]


def branches() -> Path:
    paths = get_repo_paths()
    return paths["branches"]


def store_empty():
    paths = get_repo_paths()
    return not bool(len(list(store().rglob("*"))))
