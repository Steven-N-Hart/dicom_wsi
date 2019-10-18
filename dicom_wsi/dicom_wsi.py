# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'submodules')
import logging
logger = logging.getLogger(__name__)

from parse_wsi import get_wsi
from input_validation import validate_cfg
from base_attributes import build_base
from sequence_attributes import build_sequences
from shared_functional_groups import build_functional_groups
from pixel_to_slide_conversions import add_PerFrameFunctionalGroupsSequence
from pixel_data_conversion import get_image_pixel_data

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

    for instance in range(cfg['General']['NumberOfLevels']):
        # Update config with slide attributes
        cfg, wsi = get_wsi(cfg)
        # Add the BaseAttributes
        dcm, cfg = build_base(cfg, instance=instance)
        # Add the SequenceAttributes
        dcm = build_sequences(dcm, cfg)
        # Build functional groups
        dcm = build_functional_groups(dcm, cfg)
        # Update Series Instance Attribute
        dcm.SeriesInstanceUID = dcm.SeriesInstanceUID + '.' + str(instance)
        dcm.InstanceNumber = instance
        # Add per frame functional groups
        dcm = add_PerFrameFunctionalGroupsSequence(wsi=wsi,
                                                   ds=dcm,
                                                   tile_size=cfg['General']['FrameSize'],
                                                   SeriesDownsample=instance)
        # Add Pixel data
        dcm.PixelData = get_image_pixel_data(wsi=wsi, dcm=dcm, cfg=cfg, SeriesDownsample=instance)
        print(dcm)
