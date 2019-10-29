import datetime
import logging
import tempfile

from pydicom.dataset import Dataset, FileDataset
from utils import add_data


def build_base(cfg, dcm=None, dict_element='BaseAttributes', instance=1):
    base_dict = cfg[dict_element]
    logging.debug('Beginning {} Module'.format(dict_element))
    if dict_element == 'BaseAttributes':
        suffix = '.' + str(instance) + '.dcm'
        filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name

        file_meta = Dataset()
        file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
        # file_meta.TransferSyntaxUID = '1.2.840.10008.6.1.897'

        # Create the FileDataset instance (initially no data elements, but file_meta supplied)
        dcm = FileDataset(filename_little_endian, {},
                          file_meta=file_meta, preamble=b"\0" * 128)

    # For each element in the Patient data, add to the DICOM object
    for k, v in base_dict.items():
        if v == 'NUMBER':
            cfg[dict_element][k] = 1
            v = 1
        dcm = add_data(dcm, k, v, cfg, dict_element='BaseAttributes')
    dcm.ContentDate = str(datetime.date.today()).replace('-', '')
    logging.debug('Completed {} Module'.format(dict_element))
    return dcm, cfg

