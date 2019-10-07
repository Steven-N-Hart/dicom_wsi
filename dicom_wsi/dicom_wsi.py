# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'submodules')
import logging
logger = logging.getLogger(__name__)


from input_validation import validate_cfg
from patient import build_patient
from specimen import build_specimen
from study import build_study
from general_series import build_series
from general_equipment import build_equipment


"""Main module."""
def create_dicom(cfg):
    """
    Main function for creating DICOM files
    :param cfg: dictionary containing all required variables
    :return: 0
    """
    validate_cfg(cfg)
    logger.info('All inputs are valid')
    # Build Patient info
    dcm = build_patient(cfg['Patient'])
    logger.info('Patient info is built')
    # Build Specimen info
    dcm = build_specimen(dcm, cfg['Specimen'])
    logger.info('Specimen info is built')
    # Build Study info
    dcm = build_study(dcm, cfg['GeneralStudy'])
    logger.info('Study info is built')
    # Build Series info
    dcm = build_series(dcm, cfg['GeneralSeries'])
    logger.info('Series info is built')
    # Build General Equipment info
    dcm = build_equipment(dcm, cfg['GeneralEquipment'])

    # http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_I.4.html
    VLWholeSlideMicroscopyImage = '1.2.840.10008.5.1.4.1.1.77.1.6'

    print(dcm)
