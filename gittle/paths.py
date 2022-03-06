from typing import Dict
from pathlib import Path

GITTLE = ".gittle"


def get_paths() -> Dict[str, Path]:
    cwd = Path.cwd()
    return {
        "root": cwd,
        "gittle": cwd / GITTLE,
        "store": cwd / GITTLE / "store",
    }
