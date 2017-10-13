'''
File: setup.py
Description: Bolt client installation script
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 13/10/2017
'''
from setuptools import setup, find_packages
setup(
    name='bolt_client',
    version='0.0.1',
    packages=find_packages(exclude=['docs', 'tests', 'temp'])
)
