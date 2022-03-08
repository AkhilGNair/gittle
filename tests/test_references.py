import pytest

import gittle
from gittle.paths import Paths


def test_current_branch_shows_head(repo_no_commits):
    """Test the current branch returns the contents of the HEAD file."""
    assert gittle.references.current_branch() == gittle.init.BRANCH_INITIAL


def test_catches_missing_head_file(repo_no_commits):
    """Test a gittle repo with no HEAD file is caught."""
    Paths.head.unlink()
    with pytest.raises(gittle.references.MissingGittleFile):
        assert gittle.references.current_branch()


def test_commit_with_no_commits(repo_no_commits):
    """Test that a repo with no commits conventionally returns None for the current commit."""
    assert gittle.references.current_commit() is None


def test_(repo_no_commits_with_files):
    pass
