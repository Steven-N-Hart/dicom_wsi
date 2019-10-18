import logging
import tempfile

from pydicom.dataset import Dataset, FileDataset
from utils import uid_maker, make_time, make_date, make_datetime, add_data


def build_base(cfg, dcm=None, dict_element='BaseAttributes', instance=1):
    base_dict = cfg[dict_element]
    logging.debug('Beginning {} Module'.format(dict_element))
    if dict_element == 'BaseAttributes':
        suffix = '.' + str(instance) + '.dcm'
        filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name

        file_meta = Dataset()
        # Create the FileDataset instance (initially no data elements, but file_meta supplied)
        dcm = FileDataset(filename_little_endian, {},
                          file_meta=file_meta, preamble=b"\0" * 128)

    # For each element in the Patient data, add to the DICOM object
    for k, v in base_dict.items():
        # update based on types
        if k.endswith('UID'):
            v, cfg = uid_maker(k, v, cfg, dict_element=dict_element)
        if k.endswith('Date'):
            v, cfg = make_date(k, v, cfg, dict_element=dict_element)
        if k.endswith('DateTime'):
            v, cfg = make_datetime(k, v, cfg, dict_element=dict_element)
        if k.endswith('Time') and not k.endswith('DateTime'):
            v, cfg = make_time(k, v, cfg, dict_element=dict_element)
        if v == 'NUMBER':
            v = 1
            cfg[dict_element][k] = 1
        dcm = add_data(dcm, k, v)

    logging.debug('Completed {} Module'.format(dict_element))
    return dcm, cfg, filename_little_endian
