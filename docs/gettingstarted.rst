================
Getting Started
================


Create a YAML file
-------------------

The `YAML` file contains nearly all of the required fields. This serves as a good starting point for building your DICOM conversion.
It is separated logically by DICOM Modules, followed by the DictElement representation from this `pydicom`_
dictionary.

.. _pydicom: https://github.com/pydicom/pydicom/blob/master/pydicom/_dicom_dict.py

* Note there are two special types of values for these keys:

    1. **UID**: `Use this for any key that needs a UID generated`
    2. **SQ**: `Should be set for all SQ types.`


.. code-block:: yaml

    Patient:
        PatientName: UNKNOWN
    Specimen:
        ValueType: UNKNOWN
        ContainerIdentifier: UNKNOWN
        SpecimenIdentifier: UNKNOWN
        SpecimenUID: UID
        ConceptNameCodeSequence: NULL
    ...



