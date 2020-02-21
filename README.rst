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
* Find out how to determine what `FileMetaInformationGroupLength` should be
* Thorough Unit tests
* Pass validation with dciodvfy_
* Add option to add Annotations from XML file
* Ensure Python Idioms are followed (where practical)
* Parse logic from each `file type`_ available from the OpenSlide website

  * Aperio (.svs, .tif)
  * Hamamatsu (.vms, .vmu, .ndpi)
  * Leica (.scn)
  * MIRAX (.mrxs)
  * Philips (.tiff)
  * Sakura (.svslide)
  * Trestle (.tif)
  * Ventana (.bif, .tif)
  * Generic tiled TIFF (.tif)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _dciodvfy: https://www.dclunie.com/dicom3tools/dciodvfy.html
.. _`file type`: https://openslide.org/
