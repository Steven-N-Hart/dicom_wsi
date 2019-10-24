import logging

import pyvips
from math import ceil

logger = logging.getLogger(__name__)


def get_image_pixel_data(dcm=None, cfg=None, series_downsample=0, img_obj=None):
    """
    get a compressed bitstream of the image
    :param wsi: OpenSlide Object
    :param dcm: DICOM object
    :param cfg: Config dict
    :param img_obj: specified only for when using the pixelator
    :param series_downsample: How many times to downsample
    :return: byte string to use as the pixel array
    """
    if img_obj is None:
        wsi_fn = cfg.get('General').get('WSIFile')
        out = pyvips.Image.openslideload(wsi_fn, access="sequential", level=0)  # TODO: Make this not rely on OpenSlide
        resize_level = 1 / max(1, (2 ** series_downsample))
        logger.info('Resizing to {}'.format(resize_level))
        img = out.resize(resize_level)
    else:
        logger.info('Already found image object {}'.format(img_obj))
        img = img_obj

    image_format = cfg.get('General').get('ImageFormat')
    assert image_format is not None

    compression_value = int(cfg.get('General').get('CompressionAmount'))
    compression_method = None

    if compression_value is None:
        compression_value = 0
        if image_format == 'TIFF':
            compression_method = 'ISO_15444_1'
        elif image_format == 'JPEG':
            compression_method = 'ISO_10918_1'
        else:
            raise Exception('{} files are not yet supported.'.format(image_format))

    compression_amount = 1

    if compression_value > 0:
        compression_amount = float(cfg.get('General').get('CompressionAmount'))
        assert compression_amount is not None
        assert compression_method is not None

    dcm = save_compression_params(dcm=dcm,
                                  lossy_image_compression_ratio=compression_amount,
                                  lossy_image_compression_method=compression_method)
    dcm = save_pixels(image_format=image_format, img=img, dcm=dcm, cfg=cfg)
    logger.debug('Completed writing image #################################################')
    return dcm, img


def piecewise_pixelator(img, divisor=4):
    w, h = [int(x) for x in img.__str__().split(' ')[1].split('x')]  # '<pyvips.Image 46000x32893 uchar, 4 bands, rgb>'
    h_buffer = ceil(h / divisor)
    w_buffer = ceil(w / divisor)
    logger.info('Width {} Height: {} hBuffer: {} wBuffer: {}'.format(w, h, h_buffer, w_buffer))

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


def save_pixels(image_format='TIFF', img=None, dcm=None, cfg=None):
    """

    :param image_format: TIFF or JPEG
    :param img: image object (pyvips)
    :param dcm: DICOM Object
    :param cfg: Configuration dict
    :return: dcm
    """
    if dcm.LossyImageCompression == '00':
        dcm.PixelData = img.tiffsave_buffer(bigtiff=True,
                                            tile_width=cfg.get('General').get('FrameSize'),
                                            tile_height=cfg.get('General').get('FrameSize'))
    else:
        # THe images should be compressed
        if image_format == 'TIFF':
            dcm.PixelData = img.tiffsave_buffer(Q=dcm.LossyImageCompressionRatio,
                                                bigtiff=True,
                                                tile_width=cfg.get('General').get('FrameSize'),
                                                tile_height=cfg.get('General').get('FrameSize')
                                                )
        elif image_format == 'JPEG':
            dcm.PixelData = img.jpegsave_buffer(Q=dcm.LossyImageCompressionRatio)
        else:
            raise Exception('{} files are not yet supported.'.format(image_format))
    return dcm


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

    dcm.LossyImageCompression = lossy_image_compression
    if lossy_image_compression == '01':
        dcm.LossyImageCompressionRatio = lossy_image_compression_ratio
        dcm.LossyImageCompressionMethod = lossy_image_compression_method

    return dcm
