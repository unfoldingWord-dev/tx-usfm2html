from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


with open(path.join(here, "README.rst"), "r") as f:
    long_description = f.read()

setup(
    name="tx-usfm2html",
    version="1.0.0",
    description="USFM-to-HTML conversion",
    long_description=long_description,
    url="https://github.com/unfoldingWord-dev/tx-usfm2html",
    author="unfoldingWord",
    author_email="ethantkoenig@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords=["usfm", "html"],
    packages=find_packages(),
    install_requires=["future"],
    test_suite="tests"
)
