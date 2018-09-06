import os
from codecs import open
from setuptools import setup, find_packages


here_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here_dir, "src", "vk_client", "__about__.py")) as f:
    exec(f.read(), about)

tests_deps = [
    "tox",
    "pytest"
]


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    install_requires=[
        "arrow",
        "cached-property",
        "six",
        "enum34",
        "more-itertools",
        "vk",
        "requests",
        "Pillow",
    ],
    tests_require=tests_deps,
    extras_require={
        "tests": tests_deps
    }
)
