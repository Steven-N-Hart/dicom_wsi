================
Getting Started
================


Create a YAML file
-------------------

The `YAML` file contains nearly all of the required fields. It does not need those with the
`SQ` tag.  This serves as a good starting point for building your DICOM conversion.
It is separated logically by DICOM Modules, followed by the DictElement representation from this `pydicom`_
dictionary.

.. _pydicom: https://github.com/pydicom/pydicom/blob/master/pydicom/_dicom_dict.py

.. code-block:: yaml

    Patient:
        PatientName: UNKNOWN
    Specimen:
        ValueType: UNKNOWN
        ContainerIdentifier: UNKNOWN
        SpecimenIdentifier: UNKNOWN
    ...



