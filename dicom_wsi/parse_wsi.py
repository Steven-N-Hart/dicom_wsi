from submodules.input_validation import restricted_inputs


def get_wsi(cfg):
    """
    Update the YAML defaults with image-specific attributes

    :param cfg:
    :return: cfg, wsi_object
    """
    if cfg['General']['WSIBrand'] == 'aperio_svs':
        cfg, wsi = _parse_aperio_svs(cfg)
    elif cfg['General']['WSIBrand'] == 'phillips_tiff':
        cfg, wsi = _parse_phillips_tiff(cfg)
    else:
        raise ValueError('Only acceptable files are: {}'.format(', '.join(restricted_inputs['WSIBrand'])))


def _parse_aperio_svs(cfg):
    wsi = opsenslide.OpenSlide(cfg['General']['WSIFile'])
    return cfg, wsi


def _parse_phillips_tiff(cfg):
    wsi = opsenslide.OpenSlide(cfg['General']['WSIFile'])
    return cfg, wsi
    pass
