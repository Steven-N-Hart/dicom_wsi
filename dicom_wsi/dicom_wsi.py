# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'submodules')
from parse_wsi import get_wsi
import logging
logger = logging.getLogger(__name__)

from input_validation import validate_cfg
from base_attributes import build_base

"""Main module."""
def create_dicom(cfg):
    """
    Main function for creating DICOM files
    :param cfg: dictionary containing all required variables
    :return: 0
    """
    logger.info('Beginning validation')
    validate_cfg(cfg)
    logger.info('All inputs are valid')

    # Update config with slide attributes
    cfg, wsi = get_wsi(cfg)
    exit()
    dcm = build_base(cfg['BaseAttributes'])
    logger.info('BaseAttributes info is built')

    print(dcm)
