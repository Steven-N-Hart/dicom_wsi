import logging

import pyvips

logger = logging.getLogger(__name__)


def get_image_pixel_data(dcm=None, cfg=None, series_downsample=1):
    """
    get a compressed bitstream of the image
    :param wsi: OpenSlide Object
    :param dcm: DICOM object
    :param cfg: Config dict
    :param series_downsample: How many times to downsample
    :return: byte string to use as the pixel array
    """
    wsi_fn = cfg.get('General').get('WSIFile')
    out = pyvips.Image.openslideload(wsi_fn, access="sequential", level=0)  # TODO: Make this not rely on OpenSlide
    resize_level = 1 / max(1, (2 ** series_downsample))
    logger.info('Resizing to {}'.format(resize_level))
    img = out.resize(resize_level)

    compression_value = int(cfg.get('General').get('CompressionAmount'))
    if compression_value is None:
        compression_value = 0

    compression_amount = 1

    if compression_value > 0:
        compression_amount = float(cfg.get('General').get('CompressionAmount'))
        assert compression_amount is not None

    image_format = cfg.get('General').get('ImageFormat')
    assert image_format is not None

    if image_format == 'TIFF':
        if compression_value == 0:
            dcm.LossyImageCompression = '00'
            dcm.PixelData = img.tiffsave_buffer(bigtiff=True,
                                                tile_width=cfg.get('General').get('FrameSize'),
                                                tile_height=cfg.get('General').get('FrameSize'))
        else:
            dcm.LossyImageCompression = '01'
            dcm.LossyImageCompressionRatio = compression_amount
            dcm.LossyImageCompressionMethod = 'ISO_15444_1'
            dcm.PixelData = img.tiffsave_buffer(Q=compression_amount, bigtiff=True,
                                                tile_width=cfg.get('General').get('FrameSize'),
                                                tile_height=cfg.get('General').get('FrameSize')
                                                )

    elif image_format == 'JPEG':
        dcm.LossyImageCompression = '01'
        dcm.LossyImageCompressionRatio = compression_amount
        dcm.LossyImageCompressionMethod = 'ISO_10918_1'
        dcm.PixelData = img.jpegsave_buffer(Q=compression_amount)
    else:
        raise Exception('{} files are not yet supported.'.format(image_format))
    logger.debug('Completed writing image #################################################')
    return dcm
