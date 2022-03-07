from pathlib import Path

GITTLE = ".gittle"
REFERENCES = "references"


class _Paths:
    @property
    def root(self) -> Path:
        return Path.cwd()

    @property
    def gittle(self) -> Path:
        return self.root / GITTLE

    @property
    def store(self) -> Path:
        return self.gittle / "store"

    @property
    def head(self) -> Path:
        return self.gittle / "HEAD"

    @property
    def staging(self) -> Path:
        return self.gittle / ".stage"

    @property
    def references(self) -> Path:
        return self.gittle / REFERENCES

    @property
    def branches(self) -> Path:
        return self.references / "branches"


def store_empty() -> bool:
    return not bool(len(list(Paths.store.rglob("*"))))


Paths = _Paths()
