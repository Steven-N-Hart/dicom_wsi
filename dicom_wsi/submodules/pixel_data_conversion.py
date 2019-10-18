import pyvips


def get_image_pixel_data(wsi=None, dcm=None, cfg=None, SeriesDownsample=1):
    """
    get a compressed bitstream of the image
    :param wsi: OpenSlide Object
    :param dcm: DICOM object
    :param cfg: Config dict
    :param SeriesDownsample: How many times to downsample
    :return: byte string to use as the pixel array
    """
    wsi_fn = cfg.get('General').get('WSIFile')
    out = pyvips.Image.openslideload(wsi_fn, access="sequential", level=0)
    resize_level = 1 / max(1, (2 ** SeriesDownsample - 1))
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
            img_buffer = img.tiffsave_buffer(compression=compression_amount, bigtiff=True)
        else:
            dcm.LossyImageCompression = '01'
            dcm.LossyImageCompressionRatio = compression_amount
            dcm.LossyImageCompressionMethod = 'ISO_15444_1'
            img_buffer = img.tiffsave_buffer(compression=compression_amount, bigtiff=True)


    if image_format == 'JPEG':
        dcm.LossyImageCompression = '01'
        dcm.LossyImageCompressionRatio = compression_amount
        dcm.LossyImageCompressionMethod = 'ISO_10918_1'
        img_buffer = img.write_to_buffer('.jpg', Q=compression_amount)

    else:
        raise Exception('{} files are not yet supported.'.format(image_format))

    dcm.PixelData = pyvips.Image.tiffload_buffer(img_buffer, access='sequential')
    return dcm
