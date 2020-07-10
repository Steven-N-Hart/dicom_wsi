#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages
import sys
if sys.version_info < (2,7):
    sys.exit('Sorry, Python < 2.7 is not supported')

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Steven N. Hart",
    author_email='steven.n.hart@gmail.com',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Package for converting whole slide image files to dicom.",
    entry_points={
        'console_scripts': [
            'dicom_wsi=dicom_wsi.cli:main',
        ],
    },
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dicom_wsi',
    name='dicom_wsi',
    packages=find_packages(include=['dicom_wsi', 'dicom_wsi.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Steven-N-Hart/dicom_wsi',
    version='0.1.0',
    zip_safe=False,
)
