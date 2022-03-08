from gittle.paths import Paths
import gittle


def test_store_empty(repo_no_commits):
    """Tests whether the store being empty is correctly detected."""
    filename = "some_blob"

    assert gittle.paths.store_empty() is True

    (Paths.store / filename).write_text("non-empty")
    assert gittle.paths.store_empty() is False

    (Paths.store / filename).unlink()
    assert gittle.paths.store_empty() is True
