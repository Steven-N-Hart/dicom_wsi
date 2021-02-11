================
Getting Started
================

Before you can run `dicom_wsi`, you first need to gather some input data necessary for creating a valid DICOM file.
There are to ways to do this: 1.) Create a YAML file or 2.) Build a dictionary yourself.

Create a YAML file
-------------------

The `YAML` file contains two sections: `General` and `BaseAttributes`. The `General` section contains a fixed number of required fields that are used by `dicom_wsi`, whereas the `BaseAttributes` are restricted key words from the DICOM_ standard. These are cross-referenced with the `pydicom`_ dictionary.

.. _pydicom: https://github.com/pydicom/pydicom/blob/master/pydicom/_dicom_dict.py
.. _DICOM: https://dicom.innolitics.com/ciods/vl-whole-slide-microscopy-image

`General` section
````````````````````

**Definitions**

+------------------------+------------------------------------------------------+
| Term                   | Definition                                           |
+========================+======================================================+
| *WSIFile*              | Path to whole slide image file                       |
+------------------------+------------------------------------------------------+
| *OutFilePrefix*        | What prefix to use when saving the DICOM output file |
+------------------------+------------------------------------------------------+
| *NumberOfLevels*       | How many levels should be extracted (in powers of 2) |
+------------------------+------------------------------------------------------+
| *OrgUIDRoot*           | Your organizations UID root prefix                   |
+------------------------+------------------------------------------------------+
| *FrameSize*            | How many pixels should be used for DICOM frames      |
+------------------------+------------------------------------------------------+
| *MaxFrames*            | Number of frames allowed before writing to a new file|
+------------------------+------------------------------------------------------+


`BaseAttributes` section
````````````````````````
Most of the terms in this section are defined in the DICOM_ standard. Many will not need to be changed, but some always will.  Below, I highlight those terms that will likely need to be manually set.
**Definitions**

+------------------------+------------------------------------------------------+
| Term                   | Definition                                           |
+========================+======================================================+
| *PatientName*          | LastName^FirstName                                   |
+------------------------+------------------------------------------------------+
| *PatientBirthDate*     | Date format (i.e. 20000101)                          |
+------------------------+------------------------------------------------------+
| *PatientSex*           | M: Male, F: Female, O: Other                         |
+------------------------+------------------------------------------------------+
|*PatientID*             | Unique identifier for the patient                    |
+------------------------+------------------------------------------------------+
|*ReferringPhysicianName*| LastName^FirstName                                   |
+------------------------+------------------------------------------------------+
|*StudyDate*             | Date format                                          |
+------------------------+------------------------------------------------------+
|*StudyID*               | Human readable study name                            |
+------------------------+------------------------------------------------------+

A full example can be found in `yaml/base.yaml`.

Without a YAML file
-------------------

While a `YAML` file is recommended, you don't actually need one.  You could choose
to make the dictionary yourself. The dictionary has two nested components, `General` and `BaseAttributes`,
each of which has the elements defined in `yaml/base.yaml`.


Using in existing code
-------------------

To use dicom-wsi in a project:

.. code-block:: python

    from yaml import load, BaseLoader
    import dicom_wsi
    dwsi = dicom_wsi.dicom_wsi
    get_wsi = dicom_wsi.parse_wsi.get_wsi

    # Define your YAML file
    my_yaml = '/path/to/yaml'
    # Load your YAML file
    cfg = load(open(my_yaml), Loader=BaseLoader)
    # Read the WSI, updating the config with information contained in the slide
    cfg, wsi = get_wsi(cfg)
    # Create DICOM files
    dwsi.create_dicom(cfg)


Sample RUN
-------------------
This Step will download the sample svs file
python ./tests/__init__.py

This is sample execution
python cli.py -y ./tests/testfiles/base.yaml
