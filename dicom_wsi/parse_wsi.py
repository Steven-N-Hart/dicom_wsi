import openslide
import submodules._mapping as mp
from submodules.input_validation import restricted_inputs


def get_wsi(cfg):
    """
    Update the YAML defaults with image-specific attributes

    :param cfg:
    :return: cfg, wsi_object
    """
    brand = None
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
    wsi = openslide.OpenSlide(cfg.get('General').get('WSIFile'))
    cfg = mp.map_aperio_features(cfg, wsi)
    cfg, wsi = mp.parse_aperio_compression(cfg, wsi)
    return cfg, wsi


def _parse_phillips_tiff(cfg):
    logging.error('Sorry but PhillipsTIFF files haven\'t been coded yet')
    exit(1)
    wsi = openslide.OpenSlide(cfg.get('General').get('WSIFile'))
    return cfg, wsi
