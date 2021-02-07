from setuptools import setup, find_packages

setup(
    name="revisionary",
    version="0.0.1",
    description="Tiny tool for handling version numbering in Git projects",
    license="MIT",
    author="Niko Pietikäinen",
    author_email="niko.pietikainen@protonmail.com",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
