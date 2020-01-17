import openslide
import pyvips
import logging

import mapping as mp
from input_validation import restricted_inputs

logger = logging.getLogger(__name__)


def get_wsi(cfg):
    """
    Update the YAML defaults with image-specific attributes

    :param cfg:
    :return: cfg, wsi_object
    """
    brand = cfg.get('General').get('WSIBrand')
    assert brand is not None, "Must specify a WSIBrand, you specified {}".format(brand)
    if brand == 'aperio_svs':
        cfg, wsi = _parse_aperio_svs(cfg)
    elif brand == 'phillips_tiff':
        cfg, wsi = _parse_phillips_tiff(cfg)
    else:
        raise ValueError('Only acceptable files are: {}'.format(', '.join(restricted_inputs['WSIBrand'])))
    return cfg, wsi


def _parse_aperio_svs(cfg):
    wsi_fn = cfg.get('General').get('WSIFile')
    wsi = pyvips.Image.new_from_file(wsi_fn, access='sequential')
    cfg = mp.map_aperio_features(cfg, wsi)
    return cfg, wsi


def _parse_phillips_tiff(cfg):
    logging.error('Sorry but PhillipsTIFF files haven\'t been coded yet')
    exit(1)
    wsi = openslide.OpenSlide(cfg.get('General').get('WSIFile'))
    return cfg, wsi
