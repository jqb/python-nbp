# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages


setup(
    name='nbp',
    version='1.0',
    description='Polish National Bank currency rate downloader.',
    author='Kuba Janoszek',
    author_email='kuba.janoszek@gmail.com',
    url='https://github.com/jqb/python-nbp/tree/ver-1.0',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    setup_requires=['setuptools_git'],
    zip_safe=False,
    )
