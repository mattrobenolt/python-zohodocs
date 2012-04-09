#!/usr/bin/env python
"""
Python library for interfacing with the Zoho Docs API.
"""
from setuptools import setup

setup(
    name='zohodocs',
    version='0.1.0',
    description=__doc__,
    author='Matt Robenolt',
    author_email='matt@ydekproductions.com',
    packages=[
        'zohodocs',
    ],
    package_dir={
        'zohodocs': 'zohodocs',
    },
    license='MIT',
    url='https://github.com/mattrobenolt/python-zohodocs',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires='requests',
)
