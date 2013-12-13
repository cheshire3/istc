"""Setup Cheshire3 for ISTC.

Although Cheshire3 for ISTC is not a pure Python package,
needing to be unpacked and used in situ, the convention of using setup.py
as the installation method is followed.
"""

from __future__ import with_statement

import os
from os.path import abspath, dirname, join, exists, expanduser
import inspect

# Import Setuptools
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup
from istc.setuptools.commands import (develop,
                                      install,
                                      upgrade,
                                      uninstall,
                                      unavailable_command
                                      )

_name = 'istc'
_version = '3.1'

# Inspect to find current path
setuppath = inspect.getfile(inspect.currentframe())
setupdir = os.path.dirname(setuppath)

# Requirements
with open(os.path.join(setupdir, 'requirements.txt'), 'r') as fh:
    _install_requires = fh.readlines()


setup(
    name = _name,
    version = _version,
    description = 'Cheshire3 for ISTC',
    packages=[],
    requires=['cheshire3'],
    install_requires=_install_requires,
    extras_require={
          'docs': ["sphinx"],
    },
    entry_points={
        'console_scripts': [
            'istc-serve = istc.deploy.serve:main'
        ],
    },
    author = 'John Harrison',
    author_email = u'john.harrison@liv.ac.uk',
    maintainer = 'John Harrison',
    maintainer_email = u'john.harrison@liv.ac.uk',
    license = "BSD",
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Internet :: Z39.50",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: Markup"
    ],
    cmdclass = {
                'bdist_egg': unavailable_command,
                'bdist_rpm': unavailable_command,
                'bdist_wininst': unavailable_command,
                'develop': develop,
                'install': install,
                'upgrade': upgrade,
                'uninstall': uninstall
                },
)
