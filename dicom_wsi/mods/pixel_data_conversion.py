import logging

logger = logging.getLogger(__name__)


def resize_wsi_image(wsi=None, series_downsample=0):
    """
    reshape the pyvips object to the desired size based on series downsample

    :param wsi: PyVIPS Object
    :param series_downsample: How many times to downsample
    :return: byte string to use as the pixel array
    """
    resize_level = 1 / max(1, (2 ** series_downsample))
    logger.debug('Resizing to {}'.format(resize_level))
    img = wsi.resize(resize_level)
    return img
