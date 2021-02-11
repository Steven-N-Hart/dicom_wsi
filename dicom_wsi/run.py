import logging
from timeit import default_timer as timer
import os
from .base_attributes import build_base
from .parse_wsi import get_wsi
from .pixel_data_conversion import resize_wsi_image
from .pixel_to_slide_conversions import add_per_frame_functional_groups_sequence
from .sequence_attributes import build_sequences
from .shared_functional_groups import build_functional_groups
from .add_annotations import add_annotations

logger = logging.getLogger(__name__)


def run_instance(instance, cfg):
    start = timer()
    logger.info('Beginning instance {}.'.format(instance))
    # Update config with slide attributes
    cfg, wsi = get_wsi(cfg)
    t_get_wsi = timer()
    logger.debug('Updating config with slide attributes took {} seconds.'.format(round(t_get_wsi - start, 1)))

    # Add the BaseAttributes and set the file metadata
    dcm, cfg = build_base(cfg, instance=instance)
    t_get_base = timer()
    logger.debug('Updating base attributes took {} seconds.'.format(round(t_get_base - t_get_wsi, 1)))

    # Add the SequenceAttributes
    dcm = build_sequences(dcm)
    t_get_seq = timer()
    logger.debug('Updating sequence attributes took {} seconds.'.format(round(t_get_seq - t_get_base, 1)))

    # Build functional groups
    dcm = build_functional_groups(dcm, cfg)
    t_get_func = timer()
    logger.debug('Updating functional groups took {} seconds.'.format(round(t_get_func - t_get_seq, 1)))

    # Update Series Instance Attribute
    dcm.SeriesInstanceUID = dcm.SeriesInstanceUID + '.' + str(instance)
    dcm.InstanceNumber = instance
    dcm.SeriesNumber = instance

    # Add Annotations if there are any
    anno_file = cfg.get('General').get('Annotations')
    if anno_file != "" and anno_file != None and os.path.exists(anno_file):
        logger.info('Annotations found!')
        dcm = add_annotations(dcm, cfg, instance)
    else:
        logger.info('No Annotations found')
    t_add_ann = timer()
    logger.debug('Adding annotations (if there were any) took {} seconds.'.format(round(t_add_ann - t_get_func, 1)))

    # Resize image
    img = resize_wsi_image(wsi=wsi, series_downsample=instance)
    t_get_pixels = timer()
    logger.debug('Updating pixels took {} seconds.'.format(round(t_get_pixels - t_get_func, 1)))

    logger.debug('file_meta: {}'.format(dcm.file_meta))

    # Add per frame functional groups
    add_per_frame_functional_groups_sequence(img=img,
                                             ds=dcm,
                                             cfg=cfg,
                                             tile_size=cfg.get('General').get('FrameSize'),
                                             series_downsample=instance)
    t_save = timer()

    logger.info('Total elapsed time: {} minutes.'.format(round((t_save - start) / 60, 3)))
    return 0

