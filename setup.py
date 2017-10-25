'''
File: setup.py
Description: Bolt client installation script
Author: Saurabh Badhwar <sbadhwar@redhat.com>
Date: 13/10/2017
'''
from setuptools import setup, find_packages
setup(
    name='bolt_client',
    version='1.0.0_beta',
    packages=find_packages(exclude=['docs', 'tests', 'temp'])
)
