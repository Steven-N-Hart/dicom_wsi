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
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.77.1.6'
        file_meta.MediaStorageSOPInstanceUID = '1.2.276.0.7230010.3.1.4.8323329.17698.1572316882.287667'
        file_meta.FileMetaInformationVersion = b'\x00\x01'
        file_meta.ImplementationClassUID = '1.2.276.0.7230010.3.0.3.6.2'
        file_meta.ImplementationVersionName = 'OFFIS_DCMTK_362'
        file_meta.FileMetaInformationGroupLength = 202
        # Create the FileDataset instance (initially no data elements, but file_meta supplied)
        dcm = FileDataset(filename_little_endian, {},
                          file_meta=file_meta, preamble=b"\0" * 128)

    # For each element in the Patient data, add to the DICOM object
    for k, v in base_dict.items():
        dcm = add_data(dcm, k, v, cfg, dict_element='BaseAttributes')
    dcm.ContentDate = str(datetime.date.today()).replace('-', '')
    logging.debug('Completed {} Module'.format(dict_element))
    return dcm, cfg

