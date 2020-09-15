===========================
Extracting Annotations/Images from DICOM
===========================

Extract Annotations from DICOM
------------------------------

The following script will parse the DICOM file to extract annotations and returns the annotations
in a python dictionary object.


.. code-block:: console

    $ python  ./dicom_wsi/mods/extract_annotations.py -D <Path to Dicom file>
    $ python ./dicom_wsi/mods/extract_annotations.py -D ./tests/output.6-0.dcm


Extract Images from Dicom
-------------------------

The following script will parse the DICOM file to extract images and write them
to a specified directory.



.. code-block:: console

    $ python  ./dicom_wsi/mods/extract_annotations.py -D <Path to Dicom file> -d <Path to output directory>
