=========
dicom_wsi
=========


.. image:: https://img.shields.io/pypi/v/dicom_wsi.svg
        :target: https://pypi.python.org/pypi/dicom_wsi

.. image:: https://img.shields.io/travis/Steven-N-Hart/dicom_wsi.svg
        :target: https://travis-ci.com/Steven-N-Hart/dicom_wsi

.. image:: https://readthedocs.org/projects/dicom-wsi/badge/?version=latest
        :target: https://dicom-wsi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

----------

Package for converting whole slide image files to DICOM.

* Free software: MIT license
* Documentation: https://dicom-wsi.readthedocs.io.

=====
Usage
=====

First, you need to install dicom_wsi and its dependencies. See this link_ for details.

.. _link: https://dicom-wsi.readthedocs.io/en/latest/installation.html

To use dicom-wsi:

.. code-block:: console

    python cli.py -w <WSI File path> -o <OutputDirectory> -p <output file prefix> -y yaml/base.yaml


That's it! Most of the time you wan't need to change anything. But if you do, please see the example yaml_ file.

.. _yaml: https://github.com/Steven-N-Hart/dicom_wsi/blob/master/dicom_wsi/yaml/base.yaml

Features
--------
* Validate DICOM elements using pydicom_
* Output format DICOM formatted files (vetted with dciodvfy_)

TODO
--------
* Find out how to determine what `FileMetaInformationGroupLength` should be


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _dciodvfy: https://www.dclunie.com/dicom3tools/dciodvfy.html
.. _`file type`: https://openslide.org/
.. _pydicom: https://pydicom.github.io/
