from functools import lru_cache
from pathlib import Path
from typing import Dict

GITTLE = ".gittle"
REFERENCES = "references"


@lru_cache(maxsize=None)
def _get_repo_paths() -> Dict[str, Path]:
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
    paths = _get_repo_paths()
    return paths["root"]


def gittle() -> Path:
    paths = _get_repo_paths()
    return paths["gittle"]


def store() -> Path:
    paths = _get_repo_paths()
    return paths["store"]


def staging() -> Path:
    paths = _get_repo_paths()
    return paths["staging"]


def head() -> Path:
    paths = _get_repo_paths()
    return paths["head"]


def workspace() -> Path:
    paths = _get_repo_paths()
    return paths["workspace"]


def branches() -> Path:
    paths = _get_repo_paths()
    return paths["branches"]


def store_empty():
    return not bool(len(list(store().rglob("*"))))
