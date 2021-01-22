===========================
Working with iSyntax files
===========================

I you are like me and are stuck with iSyntax files, then they first need to be converted to TIFF. The following script
will parse the isyntax file to make a config file and a BigTiff file.

First, change directories so you are in the isyntax directory of this repo , and download an example iSyntax file from
the `Phillips Website`_.

.. _`Phillips Website`: https://www.openpathology.philips.com/resources/

.. code-block:: console

   $ cd isyntax
   $ curl -o ex1.isyntax  https://www.openpathology.philips.com/wp-content/uploads/AnimalSlides/1.isyntax


Next, get the Phillips SDK. You need to create a _`log in` first.

.. `log in`_ https://www.openpathology.philips.com/login/

You will need to follow the installation instructions for your specific operating system.  Once you have it installed,
open a python terminal and run:

.. code-block:: python

    import pixelengine

If you get `ModuleNotFoundError: No module named 'pixelengine'` then you do not have this installed properly. Ask Phillips tech support for help.

> Note you need to ensure that you have the Phillips SDK installed and available. It is not possible for this toolkit


Once you have the Phillips SDK installed, you can run the conversion script.

.. code-block:: console

    $ python isyntax_to_tiff.py --input 1.isyntax --tif BIGTIFF --sparse 0  --startlevel 0

This will create a file called `ex1_BIG_sparse.tiff`.

Now you can create the configuration file and proceed as normal.

> Note: Since the `isyntax_to_tiff.py` is maintained by Phillips, its name or usage might change. Please consult the Phillips documentation.

