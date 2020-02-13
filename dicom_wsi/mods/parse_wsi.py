import openslide
import pyvips
import logging

import mapping as mp

logger = logging.getLogger(__name__)


def get_wsi(cfg):
    """
    Update the YAML defaults with image-specific attributes

    :param cfg:
    :return: cfg, wsi_object
    """
    wsi_fn = cfg.get('General').get('WSIFile')
    if wsi_fn.endswith('svs'):
        cfg, wsi = _parse_aperio_svs(cfg)
    else:
        msg = 'Since this is not an SVS file, it will be assumed to have all required information in the configuration'
        logger.info(msg)
        cfg, wsi = _parse_other(cfg)

    # noinspection PyUnboundLocalVariable
    return cfg, wsi


def _parse_aperio_svs(cfg):
    wsi_fn = cfg.get('General').get('WSIFile')
    wsi = pyvips.Image.new_from_file(wsi_fn, access='sequential')
    # Apply custom paring logic for SVS Files
    cfg = mp.map_aperio_features(cfg, wsi)
    return cfg, wsi


def _parse_other(cfg):
    wsi = openslide.OpenSlide(cfg.get('General').get('WSIFile'))
    return cfg, wsi
