import logging
from utils import uid_maker, make_time, make_date

def build_series(dcm, series_dict):
    logging.debug('Beginning Series Module')

    dcm.Modality = 'SM'

    if series_dict is '':
        return dcm

    if series_dict.get('SeriesInstanceUID'):
        dcm.StudyInstanceUID = uid_maker('SeriesInstanceUID', series_dict['SeriesInstanceUID'])

    logging.debug('Completed Series Module')
    return dcm
