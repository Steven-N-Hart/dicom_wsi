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
   $ wget https://www.openpathology.philips.com/wp-content/uploads/AnimalSlides/1.isyntax

Next, run the conversion script.

.. code-block:: console

    $ python isyntax_to_tiff.py --input ..\ex1.isyntax --tif BIGTIFF --sparse 0  --startlevel 0

This will create a file called `ex1_BIG_sparse.tiff`.

Now you can create the configuration file.
