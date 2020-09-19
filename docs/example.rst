===========================
Examples
===========================


Here is an end to end example

Clone the git repo

.. code-block:: console

    $ git clone https://github.com/Steven-N-Hart/dicom_wsi.git
	$ cd dicom_wsi
	$ mkdir example
	$ cd example


Downloading the svs file

.. code-block:: console

    $ wget http://openslide.cs.cmu.edu/download/openslide-testdata/Aperio/CMU-1-JP2K-33005.svs
	

getting the annotations

.. code-block:: console

    $ cp ../tests/CMU-1-JP2K-33005.xml .

Getting the input yaml file to generate the dicom file
Modifying values for params 'WSIFile','OutFilePrefix','Annotations'
Annotations are optional, if you want to skip annotation remove 'Annotations' param in the base.yaml file

.. code-block:: console

    $ cat ../dicom_wsi/yaml/base.yaml |sed -e 's/tests\///g'|sed -e 's/.\///g' > base.yaml

Generating the dicom filepython ../dicom_wsi/cli.py -y base.yaml

.. code-block:: console

    $ python ../dicom_wsi/cli.py -y base.yaml

Validating the generated dicom files
Download this tool https://www.dclunie.com/dicom3tools/dciodvfy.html to validate the generated dicom files

Other functions
Extracting Annotations from Dicom file to a python dictionary(Here i'm running it on only one level Dicom file)

.. code-block:: console

    $ python  ../dicom_wsi/mods/extract_annotations.py -D output.2-0.dcm

Extracting images from Dicom file

.. code-block:: console

    $ python  ../dicom_wsi/mods/extract_image_patches.py -D output.2-0.dcm -d output_images

