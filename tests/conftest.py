import pytest
from unittest.mock import patch
from pathlib import Path
import shutil

import gittle
from gittle.paths import Paths


ROOT = Path(__file__).parents[1]
PROJECT_ROOT = ROOT / "tests" / "workspace"


def cleanup(root):
    shutil.rmtree(root)
    root.mkdir()
    (root / ".gitkeep").touch()


@pytest.fixture()
def repo():
    with patch("gittle.paths.Path.cwd") as cwd:
        cwd.return_value = PROJECT_ROOT
        yield
        cleanup(PROJECT_ROOT)


@pytest.fixture()
def repo_no_commits():
    with patch("gittle.paths.Path.cwd") as cwd:
        cwd.return_value = PROJECT_ROOT
        gittle.init.create_repo()
        yield
        cleanup(PROJECT_ROOT)


@pytest.fixture()
def staged_files():
    return [".hidden/hidden.txt", "src/__init__.py"]


@pytest.fixture()
def repo_no_commits_with_files(staged_files, repo_no_commits):
    (Paths.root / "src").mkdir(exist_ok=True)
    (Paths.root / ".hidden").mkdir(exist_ok=True)

    (Paths.root / "src" / "__init__.py").write_text('print("hi")\n')
    (Paths.root / ".hidden" / "hidden.txt").write_text("# This file is hidden")
    (Paths.root / ".names").write_text("akhil:akhil@domain.com")

    Paths.staging.write_text("\n".join(staged_files))

    yield


@pytest.fixture()
def repo_with_commit(repo_no_commits_with_files, staged_files):
    gittle.commit.take_snapshot()
    new_stage = gittle.commit.find_files().difference(staged_files)
    Paths.staging.write_text("\n".join(new_stage))
    yield
