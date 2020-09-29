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

Install the required packages  as described `here <installation.html>`_

.. _`here`: https://dicom-wsi.readthedocs.io/en/latest/installation.html

Downloading the svs file

.. code-block:: console

    $ wget http://openslide.cs.cmu.edu/download/openslide-testdata/Aperio/CMU-1-JP2K-33005.svs
	

getting the annotations file

.. code-block:: console

    $ cp ../tests/CMU-1-JP2K-33005.xml .

Getting the input yaml file to generate the dicom file.Modifying values for params 'WSIFile','OutFilePrefix','Annotations'.

Annotations are optional, if you want to skip annotations, then remove 'Annotations' param in the base.yaml file
Below command will replace the paths for params 'WSIFile','OutFilePrefix','Annotations' to current directory

.. code-block:: console

    $ cat ../dicom_wsi/yaml/base.yaml |sed -e 's/tests\///g'|sed -e 's/.\///g' > base.yaml

Running the dicom_wsi tool & generating the dicom files

.. code-block:: console

    $ python ../dicom_wsi/cli.py -y base.yaml

Following dicom files will be generated (Multiple dicom files for multiple levels).

.. code-block:: console

    $ ls output.*.dcm

| output.0-10.dcm  
| output.0-2.dcm  
| output.0-6.dcm  
| output.1-1.dcm  
| output.3-0.dcm 
| output.0-11.dcm  
| output.0-3.dcm  
| output.0-7.dcm  
| output.1-2.dcm  
| output.4-0.dcm 
| output.0-12.dcm  
| output.0-4.dcm  
| output.0-8.dcm  
| output.1-3.dcm  
| output.5-0.dcm 
| output.0-1.dcm   
| output.0-5.dcm  
| output.0-9.dcm  
| output.2-0.dcm  
| output.6-0.dcm

Optional: Validating the generated dicom files.

Download this tool  `dciodvfy`_  to validate the generated dicom files

.. _`dciodvfy`: https://www.dclunie.com/dicom3tools/dciodvfy.html

Other functions
---------------

Extracting Annotations from Dicom file to a python dictionary(Here i'm running it on only one level Dicom file)

.. code-block:: console

    $ python  ../dicom_wsi/mods/extract_annotations.py -D output.2-0.dcm

Extracting images from Dicom file

.. code-block:: console

    $ python  ../dicom_wsi/mods/extract_image_patches.py -D output.2-0.dcm -d output_images

