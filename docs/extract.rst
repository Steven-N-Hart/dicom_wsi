===========================
Extracting Annotations & Images from DICOM Files
===========================

Extract Annotations from DICOM
------------------------------

The following script will parse the DICOM file to extract annotations and returns the annotations
in a python dictionary object.


.. code-block:: console

    $ python  dicom_wsi/mods/extract_annotations.py -D <Path to DICOM file>

or from inside a python script:

.. code-block:: python

    from dicom_wsi.mods.extract_annotations import extract_ann_dicom
    d = extract_ann_dicom('tests/output.6-0.dcm')   # Change this to your dicom file



Extract Images from Dicom
-------------------------

The following script will parse the DICOM file to extract images and write them
to a specified directory.


.. code-block:: console

    $ python  ./dicom_wsi/mods/extract_image_patches.py -D <Path to Dicom file> -d <Path to output directory>
