============
Installation
============

.. important:: The libvips_ and OpenSlide_ packages are required, but not available on PyPi. You will need to make sure your environment has these packages available.

.. important:: Windows is *VERY* finicky with OpenSlide_, and it's not always straightforward. The recommended way for windows users is through Docker.

.. _PhillipsSDK: https://www.openpathology.philips.com/
.. _OpenSlide: https://openslide.org/download/
.. _libvips: https://libvips.github.io/libvips/


With Conda (Preferred)
-----------------------

The preferred method uses miniconda_ because there are several necessary modules that cannot be installed with pip. To
install miniconda_:

.. _miniconda: https://docs.conda.io/en/latest/miniconda.html


.. code-block:: console

    $ sudo apt-get update
    $ wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh;
    $ bash miniconda.sh -b -p $HOME/miniconda
    $ source "$HOME/miniconda/etc/profile.d/conda.sh"
    $ hash -r
    $ conda config --set always_yes yes --set changeps1 no
    $ conda update -q conda

Once conda is installed, then you can install `dicom_wsi`:

.. code-block:: console

    $ conda config --add channels bioconda
    $ conda config --add channels conda-forge
    $ conda create -q -n test-environment python pyvips openjpeg libtiff
    $ conda activate test-environment
    $ pip install -U -r requirements_dev.txt



If using iSyntax files, you also need libtiff
http://download.osgeo.org/libtiff/tiff-4.1.0.zip


Stable release
--------------

To install dicom-wsi, run this command in your terminal (assuming you already have the non-pip installed libraries):

.. code-block:: console

    $ pip install dicom_wsi

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


With Docker
-----------
You can also build a container using Docker:

.. code-block:: console

    $ docker build -t stevennhart/dicom_wsi .

Development with PyCharm
------------------------
If you are going to do some development work with PyCharm, you will need to copy the binary files into your venv.
