from gittle.paths import Paths
import gittle


def test_repo_initialised(repo):
    """Tests the repo is created."""
    gittle.init.create_repo()
    assert Paths.gittle.exists() is True
    assert Paths.store.exists() is True
    assert Paths.head.read_text() == gittle.init.BRANCH_INITIAL
