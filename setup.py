from setuptools import setup, find_packages

tests_deps = [
    "tox",
    "pytest"
]

setup(
    name="vk-client",
    version="0.0.1",
    description="VK Python SDK.",
    # long_description="",  # TODO: Add long description
    packages=find_packages("src"),
    package_dir={"": "src"},
    # url="",  # TODO: Add repo url
    author="Suenweek",
    author_email="suenweek@protonmail.com",
    install_requires=[
        "attrs",
        "six",
        "enum34",
        "more-itertools",
        "vk"
    ],
    tests_require=tests_deps,
    extras_require={
        "tests": tests_deps
    }
)
