# -*- coding: utf-8 -*-
import logging
from timeit import default_timer as timer

from submodules.base_attributes import build_base
from submodules.input_validation import validate_cfg
from submodules.parse_wsi import get_wsi
from submodules.pixel_data_conversion import resize_wsi_image
from submodules.pixel_to_slide_conversions import add_PerFrameFunctionalGroupsSequence
from submodules.sequence_attributes import build_sequences
from submodules.shared_functional_groups import build_functional_groups

logger = logging.getLogger(__name__)

"""Main module."""

def create_dicom(cfg):
    """
    Main function for creating DICOM files
    :param cfg: dictionary containing all required variables
    :return: 0
    """
    start = timer()
    logger.debug('Beginning validation')
    validate_cfg(cfg)
    logger.info('All inputs are valid')
    number_of_levels = int(cfg.get('General').get('NumberOfLevels'))
    for instance in reversed(range(number_of_levels)):
        # for instance in range(number_of_levels):

        logger.info('Beginning instance {}.'.format(instance))
        # Update config with slide attributes
        cfg, wsi = get_wsi(cfg)  # TODO: Add tests
        t_get_wsi = timer()
        logger.debug('Updating config with slide attributes took {} seconds.'.format(round(t_get_wsi - start, 1)))

        # Add the BaseAttributes and set the file metadata
        dcm, cfg = build_base(cfg, instance=instance)  # TODO: Add tests
        t_get_base = timer()
        logger.debug('Updating base attributes took {} seconds.'.format(round(t_get_base - t_get_wsi, 1)))

        # Add the SequenceAttributes
        dcm = build_sequences(dcm, cfg)  # TODO: Add tests
        t_get_seq = timer()
        logger.debug('Updating sequence attributes took {} seconds.'.format(round(t_get_seq - t_get_base, 1)))

        # Build functional groups
        dcm = build_functional_groups(dcm, cfg)  # TODO: Add tests
        t_get_func = timer()
        logger.debug('Updating functional groups took {} seconds.'.format(round(t_get_func - t_get_seq, 1)))

        # Update Series Instance Attribute
        dcm.SeriesInstanceUID = dcm.SeriesInstanceUID + '.' + str(instance)
        dcm.InstanceNumber = instance
        dcm.SeriesNumber = instance

        # Resize image
        img = resize_wsi_image(wsi=wsi, series_downsample=instance)
        t_get_pixels = timer()
        logger.debug('Updating pixels took {} seconds.'.format(round(t_get_pixels - t_get_func, 1)))

        # Add per frame functional groups
        add_PerFrameFunctionalGroupsSequence(img=img,
                                             ds=dcm,
                                             cfg=cfg,
                                             tile_size=cfg.get('General').get('FrameSize'),
                                                   series_downsample=instance)  # TODO: Add tests
        t_save = timer()

        logger.info('Total elapsed time: {} minutes.'.format(round((t_save - start) / 60, 3)))
        exit(1)
