=====
TL;DR
=====

To use dicom-wsi in a project, you can run in one of two ways. You can run the command line program,

.. code-block:: console

    python cli.py -w <WSI File path> -o <OutputDirectory> -p <output file prefix> -y yaml/base.yaml

Or you can run it directly from python

.. code-block:: python

    import dicom_wsi
    dicom_wsi.dicom_wsi.create_dicom(cfg, pools=n_pools)

The `cfg` is the dictionary of required entities, and n_pools defines the number of threads to use.

That's it!
