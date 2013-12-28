# -*- coding: utf-8 -*-
"""Installer for the worklogparser package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'HISTORY.rst') + \
    read('docs', 'LICENSE')

setup(
    name='worklogparser',
    version='0.1',
    description='Work Log Parser',
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
    ],
    keywords='Plone HUD Panels',
    author='Matej Cotman',
    author_email='cotman.matej@gmail.com',
    url='https://github.com/matejc/worklogparser',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'jinja2',
        'setuptools',
    ],
    tests_require=[
        'mock',
        'nose',
        'unittest2'
    ],
    entry_points={
        'console_scripts': [
            'worklogparser = worklogparser.work:main',
        ]
    },
    test_suite='nose.collector',
    package_data={
        'worklogparser':
        [
            'templates/long_report.jinja',
            'templates/short_report.jinja',
            'templates/weekly_report.jinja',
            'tests/testdata/example-2013.txt',
        ]
    },
)
