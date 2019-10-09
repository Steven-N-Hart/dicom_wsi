import logging
from utils import uid_maker, make_time, make_date
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence

def build_whole_slide_microscopy_image(dcm, wsmi_dict, general_dict):
    logging.debug('Beginning WSMI Module')

    ds1 = Dataset()

    logging.debug('Completed WSMI Module')
    return dcm
