from pathlib import Path
import hashlib
import zlib

from gittle import paths, references, stage


def make_hash(content, hash_length=8):
    hash = hashlib.sha1(content)
    return hash.hexdigest()[:hash_length]


def _store(hash, content):
    path = paths.store() / hash
    path.write_bytes(zlib.compress(content))
    return hash


def compute_address(file):
    content = Path(file).read_bytes()
    hash = make_hash(content)
    return hash, content


def store_file(file):
    return _store(*compute_address(file))


def store_snapshot(hashes):
    content = "\n".join(hashes).encode()
    hash = make_hash(content)
    return _store(hash=hash, content=content)


def take_snapshot():
    """Creates a snapshot of the repository."""
    hashes = [store_file(file) for file in stage.read()]
    commit = store_snapshot(hashes)
    references.update(commit=commit)
    stage.clear()
    return commit


def read_snapshot(snapshot):
    content = (paths.store() / snapshot).read_bytes()
    return set(zlib.decompress(content).decode("utf-8").split("\n"))
