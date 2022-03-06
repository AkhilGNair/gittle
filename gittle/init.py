from .paths import get_paths


def init() -> None:
    paths = get_paths()

    paths["store"].mkdir(parents=True, exist_ok=True)
    (paths["gittle"] / "head").write_text("main")
