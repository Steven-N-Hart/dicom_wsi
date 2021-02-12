#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as req:
    setup_requirements = req.read()

test_requirements = setup_requirements

version = '1.0.3'

setup(
    author="Steven N. Hart",
    author_email='hart.steven@mayo.edu',
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
        'Programming Language :: Python :: 3.7',
    ],
    description="Package for converting whole slide image files to dicom.",
    entry_points={
        'console_scripts': [
            'dicom_wsi=dicom_wsi.cli:main',
        ],
    },
    install_requires=test_requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dicom_wsi',
    name='dicom_wsi',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Steven-N-Hart/dicom_wsi',
    version=version,
    zip_safe=False,
)
