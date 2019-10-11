import logging
import tempfile

from pydicom.dataset import Dataset, FileDataset
from utils import uid_maker, make_time, make_date, make_datetime, add_data


def build_base(base_dict):
    logging.debug('Beginning BaseAttributes Module')
    suffix = '.dcm'
    filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name

    file_meta = Dataset()
    # Create the FileDataset instance (initially no data elements, but file_meta supplied)
    ds = FileDataset(filename_little_endian, {},
                     file_meta=file_meta, preamble=b"\0" * 128)

    # For each element in the Patient data, add to the DICOM object
    for k, v in base_dict.items():
        logging.debug('Attempting to add ' + 'ds.' + str(k) + '=' + str(v))

        # update based on types
        if k.endswith('UID'):
            v = uid_maker(k, v)
        if k.endswith('Date'):
            v = make_date(v)
        if k.endswith('DateTime'):
            v = make_datetime(v)
        if k.endswith('Time') and not k.endswith('DateTime'):
            v = make_time(v)

        ds = add_data(ds, k, v)

    logging.debug('Completed BaseAttributes Module')
    return ds
