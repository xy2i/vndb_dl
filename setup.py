# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='vndb_dl',
    version='0.1.0',
    description='Download visual novel metadata and screenshots from vndb.org',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='xy2_',
    author_email='xy2trezatreza@gmail.com',
    url='https://github.com/xy2iii/vndb_dl',
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={'console_scripts': ['vndb_dl = vndb_dl:main.main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "beautifulsoup4",
        "requests"
    ]
)