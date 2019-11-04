import re

from submodules import utils


def map_aperio_features(cfg, wsi):
    """
    Update attributes by mapping from vendor specific attributes to DICOM attributes
    :param cfg:
    :param wsi:
    :return:
    """
    tmp = cfg.get('BaseAttributes').get('Manufacturer')
    if tmp is None:
        cfg['BaseAttributes']['Manufacturer'] = None
    else:
        cfg['BaseAttributes']['Manufacturer'] = tmp
    tmp = cfg.get('BaseAttributes').get('SeriesDescription')
    if tmp is None:
        cfg['BaseAttributes']['SeriesDescription'] = wsi.get_value('openslide.vendor')
    _, cfg = utils.make_time('ContentTime', wsi.get_value('aperio.Date'), cfg)
    _, cfg = utils.make_time('StudyTime', wsi.get_value('aperio.Date'), cfg)
    _, cfg = utils.make_time('SeriesTime', wsi.get_value('aperio.Date'), cfg)
    _, cfg = utils.make_time('ContentTime', wsi.get_value('aperio.Date'), cfg)
    cfg['OnTheFly'] = dict()
    cfg['OnTheFly']['PixelMeasuresSequence'] = wsi.get_value('openslide.mpp-x'), wsi.get_value('openslide.mpp-y')

    return cfg



def parse_aperio_compression(cfg, wsi):
    """
    Find out if it is compressed and how much
    :param cfg: configuration dictionary
    :param wsi: openslide object
    :return:
    """
    # ['Aperio Image Library v11.2.1 \r\n46000x32914 [0,0 46000x32893] (240x240) ', 'J2K/KDU Q=30',
    # ';CMU-1;Aperio Image Library v10.0.51\r\n46920x33014 [0,100 46000x32914] (256x256) JPEG/RGB Q=30|AppMag = 20|
    # StripeWidth = 2040|ScanScope ID = CPAPERIOCS|Filename = CMU-1|Date = 12/29/09|Time = 09:59:15|
    # User = b414003d-95c6-48b0-9369-8010ed517ba7|Parmset = USM Filter|MPP = 0.4990|Left = 25.691574|Top = 23.449873|
    # LineCameraSkew = -0.000424|LineAreaXOffset = 0.019265|LineAreaYOffset = -0.000313|Focus Offset = 0.000000|
    # ImageID = 1004486|OriginalWidth = 46920|Originalheight = 33014|Filtered = 5|OriginalWidth = 46000|
    # OriginalHeight = 32914'
    ImageDescription = wsi.get_value('tiff.ImageDescription')
    if re.search("J2K/KDU Q=[0-9]+", ImageDescription):
        compression = re.search("J2K/KDU Q=[0-9]+", ImageDescription)
        compression = ImageDescription[compression.span()[0]:compression.span()[1]]
        compression_ratio = int(compression.split('=')[1])
        compression_method = compression.split(' Q')[0]
        cfg['ConditionalAttributes'] = dict()
        cfg['ConditionalAttributes']['LossyImageCompression'] = dict()
        cfg['ConditionalAttributes']['LossyImageCompression']['01'] = dict()

        if compression_method.__contains__('J2K'):
            cfg['ConditionalAttributes']['LossyImageCompression']['01'][
                'LossyImageCompressionRatio'] = compression_ratio
            cfg['ConditionalAttributes']['LossyImageCompression']['01']['LossyImageCompressionMethod'] = 'ISO_10918_1'
        elif compression_method.__contains__('JPEG'):  # TODO Test compression method variable on JPEG compressed file
            cfg['ConditionalAttributes']['LossyImageCompression']['01'][
                'LossyImageCompressionRatio'] = compression_ratio
            cfg['ConditionalAttributes']['LossyImageCompression']['01']['LossyImageCompressionMethod'] = 'ISO_15444_1'
        else:
            cfg['ConditionalAttributes']['LossyImageCompression']['00'] = dict()
            del cfg['ConditionalAttributes']['LossyImageCompression']['01']
    return cfg, wsi
