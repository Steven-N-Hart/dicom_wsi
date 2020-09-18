import logging

import pyvips

from . import mapping as mp

logger = logging.getLogger(__name__)


def get_wsi(cfg):
    """
    Update the YAML defaults with image-specific attributes

    :param cfg:
    :return: cfg, wsi_object
    """
    wsi_fn = cfg.get('General').get('WSIFile')
    pyvips.logger.setLevel(30)
    wsi = pyvips.Image.new_from_file(wsi_fn, access='sequential')

    if wsi_fn.endswith('svs'):
        logger.debug('Assuming SVS file from file extension')
        cfg = mp.map_aperio_features(cfg, wsi)
    else:
        logger.debug('Assuming non SVS file from file extension')
        cfg = mp.map_other_features(cfg, wsi)

    # noinspection PyUnboundLocalVariable
    return cfg, wsi
