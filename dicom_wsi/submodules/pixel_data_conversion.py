import io

import numpy as np
import tiffile


def get_image_pixel_data(wsi=None, dcm=None, cfg=None, SeriesDownsample=1):
    """
    get a compressed bitstream of the image
    :param wsi: OpenSlide Object
    :param dcm: DICOM object
    :param cfg: Config dict
    :param SeriesDownsample: How many times to downsample
    :return: byte string to use as the pixel array
    """

    img = wsi.get_thumbnail(([x / (2 ** SeriesDownsample) for x in wsi.dimensions]))
    imgByteArr = io.BytesIO()

    compression_value = int(cfg.get('General').get('CompressionAmount'))
    if compression_value is None:
        compression_value = 0

    compression_amount = None

    if compression_value > 0:
        compression_amount = float(cfg.get('General').get('CompressionAmount'))
        assert compression_amount is not None

    image_format = cfg.get('General').get('ImageFormat')
    assert image_format is not None

    if image_format == 'BigTIFF':
        if compression_value == 0:
            dcm.LossyImageCompression = '00'
        else:
            dcm.LossyImageCompression = '01'
            dcm.LossyImageCompressionRatio = compression_amount
            dcm.LossyImageCompressionMethod = 'ISO_15444_1'
        img = np.asarray(img)
        tiffile.imwrite(imgByteArr, img)

    if image_format == 'JPEG':
        dcm.LossyImageCompression = '01'
        dcm.LossyImageCompressionRatio = compression_amount
        dcm.LossyImageCompressionMethod = 'ISO_10918_1'
        img.save(imgByteArr, format='JPEG', quality=compression_amount)

    if image_format == 'JPEG2000':
        img.save(imgByteArr, format='JPEG2000')

    else:
        raise Exception('{} files are not yet supported.'.format(image_format))

    dcm.PixelData = imgByteArr.getvalue()
    del imgByteArr
    return dcm
