import tempfile
import logging

from pydicom.dataset import Dataset, FileDataset, Tag

def build_patient(patient_dict):
    logging.debug('Beginning Patient Module')
    suffix = '.dcm'
    filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name

    file_meta = Dataset()
    # Create the FileDataset instance (initially no data elements, but file_meta
    # supplied)
    ds = FileDataset(filename_little_endian, {},
                     file_meta=file_meta, preamble=b"\0" * 128)

    # For each element in the Patient data, add to the DICOM object
    for k, v in patient_dict.items():
        logging.debug('Attempting to add ' + 'ds.' + str(k) + '=' + str(v))
        exec('ds.' + str(k) + '=\"' + str(v) + '\"')

    logging.debug('Completed Patient Module')
    return ds
