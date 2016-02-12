#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import tuby.core as tuby


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

packages = [
    'tuby',
]

package_data = {}

requires = []

scripts = ['script/tuby', 'script/tuby-minify-modules']

data_files = [
    ('module', [m for m in tuby.module_list(".")]),
]

classifiers = [
    #        'Development Status :: 4 - Beta',
    #        'Environment :: Web Environment',
    #        'Framework :: Django',
    #        'Intended Audience :: Developers',
    #        'License :: OSI Approved :: MIT License',
    #        'Operating System :: OS Independent',
    #        'Programming Language :: Python',
    #        'Programming Language :: Python :: 2.6',
    #        'Programming Language :: Python :: 2.7',
    #        'Topic :: Software Development :: Debuggers',
    #        'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name=tuby.__progname__,
    version=tuby.__version__,
    description=tuby.__description__,
    long_description=readme,
    packages=packages,
    package_data=package_data,
    install_requires=requires,
    author=tuby.__author__,
    author_email=tuby.__email__,
    url='',
    scripts=scripts,
    license='MIT',
    classifiers=classifiers,
    data_files=data_files,
)
