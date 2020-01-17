============
Installation
============

.. important:: The libvips_ package is required, but not available on PyPi. You will need to make sure your environment has these packages available.

.. _PhillipsSDK: https://www.openpathology.philips.com/
.. _OpenSlide: https://openslide.org/download/
.. _libvips: https://libvips.github.io/libvips/

Stable release
--------------

To install dicom-wsi, run this command in your terminal:

.. code-block:: console

    $ pip install dicom_wsi

This is the preferred method to install dicom-wsi, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for dicom-wsi can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/Steven-N-Hart/dicom_wsi

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/Steven-N-Hart/dicom_wsi/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/Steven-N-Hart/dicom_wsi
.. _tarball: https://github.com/Steven-N-Hart/dicom_wsi/tarball/master


Development with PyCharm
------------
If you are going to do some development work with PyCharm, you will need to copy the binary files into your venv.
