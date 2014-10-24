#!/usr/bin/env python
# -*- coding:utf-8 -*-

import slacksend
from setuptools import setup
from pathlib import Path

README = Path(__file__) / '..' / 'README.rst'
README = README.resolve()

setup(
    name = slacksend.name,
    py_modules = ['slacksend'],
    entry_points = {
        'console_scripts': [
            'slacksend = slacksend:main',
        ],
    },
    install_requires = ["setproctitle", "requests"],
    version = slacksend.version,
    description = slacksend.description,
    long_description = README.open().read(),
    author = "Massimiliano Torromeo",
    author_email = "massimiliano.torromeo@gmail.com",
    url = slacksend.url,
    download_url = "{}/tarball/v{}".format(slacksend.url, slacksend.version),
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Topic :: Utilities"
    ],
    license = "MIT License"
)
