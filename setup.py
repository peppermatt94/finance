# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name = 'finance',
    version = '0.1.0',
    packages = ['finance'],
    #install_requires = ["required_package", ],
    entry_points = {
        'console_scripts': [
            'finance = finance.__main__:main',
        ]
    })
