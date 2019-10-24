# -*- coding: utf-8 -*-
import logging
import os
import sys
from timeit import default_timer as timer

sys.path.insert(0, 'submodules')
from parse_wsi import get_wsi
from input_validation import validate_cfg
from base_attributes import build_base
from sequence_attributes import build_sequences
from shared_functional_groups import build_functional_groups
from pixel_to_slide_conversions import add_PerFrameFunctionalGroupsSequence
from pixel_data_conversion import get_image_pixel_data, piecewise_pixelator

logger = logging.getLogger(__name__)

"""Main module."""


def create_dicom(cfg):
    """
    Main function for creating DICOM files
    :param cfg: dictionary containing all required variables
    :return: 0
    """
    start = timer()
    logger.info('Beginning validation')
    validate_cfg(cfg)
    logger.info('All inputs are valid')
    number_of_levels = int(cfg.get('General').get('NumberOfLevels'))
    frame_size = cfg.get('General').get('FrameSize')
    for instance in reversed(range(number_of_levels)):
        logger.info('Beginning instance {}.'.format(instance))
        # Update config with slide attributes
        cfg, wsi = get_wsi(cfg)  # TODO: Handle non OpenSlide files as well
        # TODO: Add tests
        t_get_wsi = timer()
        logger.info('Updating config with slide attributes took {} seconds.'.format(round(t_get_wsi - start, 1)))

        # Add the BaseAttributes
        dcm, cfg = build_base(cfg, instance=instance)  # TODO: Add tests
        t_get_base = timer()
        logger.info('Updating base attributes took {} seconds.'.format(round(t_get_base - t_get_wsi, 1)))

        # Add the SequenceAttributes
        dcm = build_sequences(dcm, cfg)  # TODO: Add tests
        t_get_seq = timer()
        logger.info('Updating sequence attributes took {} seconds.'.format(round(t_get_seq - t_get_base, 1)))

        # Build functional groups
        dcm = build_functional_groups(dcm, cfg)  # TODO: Add tests
        t_get_func = timer()
        logger.info('Updating functional groups took {} seconds.'.format(round(t_get_func - t_get_seq, 1)))

        # Update Series Instance Attribute
        dcm.SeriesInstanceUID = dcm.SeriesInstanceUID + '.' + str(instance)
        dcm.InstanceNumber = instance

        # Add per frame functional groups
        dcm = add_PerFrameFunctionalGroupsSequence(wsi=wsi,
                                                   ds=dcm,
                                                   tile_size=frame_size,
                                                   series_downsample=instance)  # TODO: Add tests
        t_get_perframe = timer()
        logger.info('Updating per frame groups took {} seconds.'.format(round(t_get_perframe - t_get_func, 1)))

        # Add Pixel data
        dcm, img = get_image_pixel_data(dcm=dcm, cfg=cfg, series_downsample=instance)  # TODO: Add tests
        t_get_pixels = timer()
        logger.info('Updating pixels took {} seconds.'.format(round(t_get_pixels - t_get_perframe, 1)))

        # Save files
        out_file_prefix = cfg.get('General').get('OutFilePrefix')
        try:
            out_file = out_file_prefix + '.' + str(instance) + '.dcm'
            dcm.save_as(out_file)
            logger.info('Saved {}'.format(out_file))
        except Exception:
            out_file = out_file_prefix + '.' + str(instance) + '.dcm'
            if os.path.exists(out_file):
                os.remove(out_file)
            # Need to write multiple instances because the number of bytes is too large
            logger.warning('Image too large.  Writing to multiple files')
            fragment = 1
            for img_part in piecewise_pixelator(img, divisor=4):
                new_dcm = dcm
                new_dcm, _ = get_image_pixel_data(dcm=new_dcm, cfg=cfg, img_obj=img_part)
                out_file = out_file_prefix + '.' + str(instance) + '-' + str(fragment) + '.dcm'
                new_dcm.save_as(out_file)
                fragment += 1
                logger.info('Saved {}'.format(out_file))
        t_save = timer()
        logger.info('Completed instance {} in {} minutes.'.format(instance, round((t_save - t_get_wsi) / 60, 1)))
        logger.info('Total elapsed time: {} minutes.'.format(round((t_save - start) / 60, 3)))
