""" App setup
"""

import os
from setuptools import setup

def read(fname):
    """
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="flaskgur",
    version="0.0.1",
    author="",
    author_email="",
    description=("Simple image hosting site written with Flask and Python"),
    license="GPLv2",
    keywords="image Flask Python",
    url="",
    packages=['flaskgur'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    install_requires=[
        'flask==1.0',
        'pillow==9.0.0',
    ],
)
