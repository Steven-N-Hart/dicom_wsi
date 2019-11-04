import logging
from math import ceil

import numpy as np

logger = logging.getLogger(__name__)


def resize_wsi_image(cfg=None, wsi=None, series_downsample=0):
    """
    get a compressed bitstream of the image
    :param wsi: OpenSlide Object
    :param dcm: DICOM object
    :param cfg: Config dict
    :param wsi: whole slide image object
    :param series_downsample: How many times to downsample
    :return: byte string to use as the pixel array
    """
    resize_level = 1 / max(1, (2 ** series_downsample))
    logger.debug('Resizing to {}'.format(resize_level))
    img = wsi.resize(resize_level)
    image_format = cfg.get('General').get('ImageFormat')
    assert image_format is not None
    return img



def piecewise_pixelator(img, divisor=4):
    """
    This generator breaks up large image blocks into smaller ones that can be saved
    :param img: image to write
    :param divisor: Number of times to split the image into smaller parts
    :return: subset image
    """
    w, h = [int(x) for x in img.__str__().split(' ')[1].split('x')]  # '<pyvips.Image 46000x32893 uchar, 4 bands, rgb>'
    h_buffer = ceil(h / divisor)
    w_buffer = ceil(w / divisor)
    logger.debug('Width {} Height: {} hBuffer: {} wBuffer: {}'.format(w, h, h_buffer, w_buffer))

    for iteration in range(divisor):
        h_position = h_buffer * iteration
        w_position = w_buffer * iteration
        if h_position + h_buffer > h:
            h_buffer = h - h_position
        if w_position + w_buffer > w:
            w_buffer = w - w_position
        logger.info('Extracting from {} to {} and {} to {}'.format(w_position, w_position + w_buffer,
                                                                   h_position, h_position + h_buffer))
        sub_img = img.extract_area(w_position, h_position, w_buffer, h_buffer)
        yield sub_img


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


# https://libvips.github.io/pyvips/intro.html#numpy-and-pil
format_to_dtype = {
    'uchar': np.uint8,
    'char': np.int8,
    'ushort': np.uint16,
    'short': np.int16,
    'uint': np.uint32,
    'int': np.int32,
    'float': np.float32,
    'double': np.float64,
    'complex': np.complex64,
    'dpcomplex': np.complex128,
}

dtype_to_format = {
    'uint8': 'uchar',
    'int8': 'char',
    'uint16': 'ushort',
    'int16': 'short',
    'uint32': 'uint',
    'int32': 'int',
    'float32': 'float',
    'float64': 'double',
    'complex64': 'complex',
    'complex128': 'dpcomplex',
}
