# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

import nbp


setup(
    name='nbp',
    version=nbp.VERSION,
    description='Polish National Bank currency rate downloader.',
    author='Kuba Janoszek',
    author_email='kuba.janoszek@gmail.com',
    url='https://github.com/jqb/python-nbp/tree/ver-%s' % nbp.VERSION,
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
