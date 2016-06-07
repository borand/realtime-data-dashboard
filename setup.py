# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='realtime-data-dashboard',
    version='0.0.1',
    description='Simplistic tornado/redis based web server for writing real time data dashboards',
    long_description=readme,
    author='Alan Borand',
    author_email='',
    url='https://github.com/borand/realtime-data-dashboard.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

