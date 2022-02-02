from io import open

from setuptools import setup

with open('requirements.txt', encoding='utf-8-sig') as f:
    requirements = f.readlines()

setup(
    name='PiDotTracker',
    version='0.1',
    install_requires=requirements
)
