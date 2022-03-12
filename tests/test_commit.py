import gittle
from gittle.paths import Paths

ALL_FILES = {".hidden/hidden.txt", "src/__init__.py", ".names", ".gitkeep"}
FIXTURE_FILE_HASH = "e0fa1f50"


def test_read_snapshot_with_no_commits():
    assert gittle.commit.read_snapshot(commit=None) == gittle.commit.EMPTY_SNAPSHOT


def test_content_addressable_storage(repo_no_commits):
    filename = "commit_me.py"
    (Paths.root / filename).write_text("print('a commit!')")
    hash, content = gittle.commit.content_address(filename)
    assert hash == FIXTURE_FILE_HASH


def test_find_files_returns_all(repo_no_commits_with_files):
    """Tests all files including hidden, but excluding the gittle directory are returned."""
    expected = ALL_FILES
    assert gittle.commit.find_files() == expected


def test_detect_changes_with_no_commits_returns_all_files(repo_no_commits_with_files):
    """Tests all files including hidden, but excluding the gittle directory are returned."""
    expected = ALL_FILES
    assert gittle.commit.detect_changes() == expected


def test_take_snapshot_for_first_commit(staged_files, repo_no_commits_with_files):
    commit = gittle.commit.take_snapshot()

    # Commit n files + 1 for the snapshot
    assert len(list(Paths.store.rglob("*"))) == len(staged_files) + 1

    tree = gittle.commit.read_snapshot(commit)
    assert tree["parents"] == []
    assert len(tree["content"]) == 2

    hashes = sorted(tree["content"])
    blob = gittle.commit.read_blob(commit=hashes[0])
    assert blob["file"] == "src/__init__.py"
    assert blob["content"] == 'print("hi")\n'


def test_take_snapshot_a(repo_with_commit):
    commit = gittle.commit.take_snapshot()
    tree = gittle.commit.read_snapshot(commit)

    blob = gittle.commit.read_blob(tree["parents"][0])
    print(blob)

    assert len(tree["parents"]) == 1
    assert len(tree["content"]) == 4

    print(tree["content"])

    assert tree["parents"] == ["51d833e2"]
    assert set(tree["content"]) == set(["c3852a2d", "f0a31b57", "f2473f96", "ff617618"])
