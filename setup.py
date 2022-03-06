from setuptools import setup, find_packages

__title__ = "gittle"
__description__ = "Little git"
__version__ = "0.1"

REQUIRED_PACKAGES = [
    # "click>=7.1.2",
    # "rich==9.10.0",
]

setup(
    name=__title__,
    description=__description__,
    version=__version__,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=REQUIRED_PACKAGES,
    # extras_require={"dev": DEV_PACKAGES},
    entry_points="""
        [console_scripts]
        gittle=gittle.cli:cli
    """,
)
