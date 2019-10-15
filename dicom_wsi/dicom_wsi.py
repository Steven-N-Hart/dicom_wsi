# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'submodules')
from parse_wsi import get_wsi
import logging
logger = logging.getLogger(__name__)

from input_validation import validate_cfg
from base_attributes import build_base
from sequence_attributes import build_sequences

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
    # Add the BaseAttributes
    dcm, cfg = build_base(cfg)
    # Add the SequenceAttributes
    dcm = build_sequences(dcm, cfg)
    print(dcm)
