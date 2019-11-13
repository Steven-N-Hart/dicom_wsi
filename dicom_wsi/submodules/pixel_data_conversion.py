import logging

logger = logging.getLogger(__name__)

def resize_wsi_image(wsi=None, series_downsample=0):
    """
    reshape the pyvips oject to the desired size based on series downsample

    :param wsi: PyVIPS Object
    :param dcm: DICOM object
    :param cfg: Config dict
    :param img_obj: specified only for when using the pixelator
    :param series_downsample: How many times to downsample
    :return: byte string to use as the pixel array
    """
    resize_level = 1 / max(1, (2 ** series_downsample))
    logger.debug('Resizing to {}'.format(resize_level))
    img = wsi.resize(resize_level)
    return img


def save_compression_params(dcm=None,
                            lossy_image_compression_ratio=0,
                            lossy_image_compression_method=None):
    """
    Save compression information into DICOM object
    :param dcm: DICOM Object
    :param lossy_image_compression_ratio: How much compression should be applied
    :param lossy_image_compression_method: ['ISO_15444_1', 'ISO_10918_1']
    :return: dcm
    """
    # TODO: Implement
    if lossy_image_compression_ratio == 0:
        lossy_image_compression = '00'
    else:
        lossy_image_compression = '01'

    lossy_image_compression = '00'
    dcm.LossyImageCompression = lossy_image_compression
    if lossy_image_compression == '01':
        dcm.LossyImageCompressionRatio = lossy_image_compression_ratio
        dcm.LossyImageCompressionMethod = lossy_image_compression_method

    return dcm
