from setuptools import find_namespace_packages, setup

setup(
    name="getsheet",
    version="0.1.0",
    author="Roman S",
    description="Script for transfer data from Google sheets to Redmine",
    long_descriptoin="",
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': 'getsheet=app:main'
    },
    install_requires=[]
    )
