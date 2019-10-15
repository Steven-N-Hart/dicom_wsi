=========
dicom-wsi
=========


.. image:: https://img.shields.io/pypi/v/dicom_wsi.svg
        :target: https://pypi.python.org/pypi/dicom_wsi

.. image:: https://img.shields.io/travis/Steven-N-Hart/dicom_wsi.svg
        :target: https://travis-ci.org/Steven-N-Hart/dicom_wsi

.. image:: https://readthedocs.org/projects/dicom-wsi/badge/?version=latest
        :target: https://dicom-wsi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

----------

Package for converting whole slide image files to DICOM.

* Free software: MIT license
* Documentation: https://dicom-wsi.readthedocs.io.

Features
--------
* Validate DICOM elements

TODO
--------
* Add validation for types 1C, 2, and 3
* Add byte or character size limit validation (see `size_limits` in character_validation.py)
* Test compression method variable on JPEG compressed file in _mapping.py

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
