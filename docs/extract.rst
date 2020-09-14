===========================
Extracting Annotations/Images from Dicom
===========================

Extract Annotations from Dicom
------------------------------

The following script will parse the Dicom file to extract annotations and returns the annotations in a python dictionary object.

python  ./dicom_wsi/mods/extract_annotations.py -D <Path to Dicom file>
python ./dicom_wsi/mods/extract_annotations.py -D ./tests/output.6-0.dcm
	
.. code-block:: console

    $ python  ./dicom_wsi/mods/extract_annotations.py -D <Path to Dicom file>
    $ python ./dicom_wsi/mods/extract_annotations.py -D ./tests/output.6-0.dcm
	

Extract Images from Dicom
-------------------------

The following script will parse the Dicom file to extract images and write them to a specified directory.
python  ./dicom_wsi/mods/extract_annotations.py -D <Path to Dicom file> -d <Path to output directory>
python ./dicom_wsi/mods/extract_annotations.py -D ./tests/output.6-0.dcm -d ./tests/
.. code-block:: console

    $ python  ./dicom_wsi/mods/extract_annotations.py -D <Path to Dicom file> -d <Path to output directory>
    $ python ./dicom_wsi/mods/extract_annotations.py -D ./tests/output.6-0.dcm -d ./tests/
	


