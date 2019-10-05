# -*- coding: utf-8 -*-
from submodules.input_validation import validate_cfg
import logging
logger = logging.getLogger('wsi_dicom_logger')

"""Main module."""
def create_dicom(cfg):
    """
    Main function for creating DICOM files
    :param cfg: dictionary containing all required variables
    :return: 0
    """
    validate_cfg(cfg)
    logger.info('All inputs are valid')
