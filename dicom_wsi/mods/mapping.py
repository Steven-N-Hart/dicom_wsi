import mods.utils

# =====================================================================================
# Use this piece of code to automatically parse information from different slide types
# =====================================================================================


def map_aperio_features(cfg, wsi):
    """
    Update attributes by mapping from vendor specific attributes to DICOM attributes
    :param cfg:
    :param wsi:
    :return:
    """
    cfg['OnTheFly'] = dict()
    if not cfg.get('BaseAttributes').get('Manufacturer'):
        cfg['BaseAttributes']['Manufacturer'] = wsi.get('openslide.vendor')
    if not cfg.get('BaseAttributes').get('SeriesDescription'):
        cfg['BaseAttributes']['SeriesDescription'] = str(wsi.get('aperio.ImageID'))

    if not cfg.get('BaseAttributes').get('ContentTime'):
        _, cfg = utils.make_time('ContentTime', wsi.get('aperio.Time'), cfg,
                                 dict_element='SharedFunctionalGroupsSequence')

    if not cfg.get('BaseAttributes').get('SeriesTime'):
        _, cfg = utils.make_time('SeriesTime', wsi.get('aperio.Time'), cfg,
                                 dict_element='SharedFunctionalGroupsSequence')

    if not cfg.get('BaseAttributes').get('StudyTime'):
        _, cfg = utils.make_time('StudyTime', wsi.get('aperio.Time'), cfg,
                                 dict_element='SharedFunctionalGroupsSequence')

    pv = wsi.get('openslide.mpp-x'), wsi.get('openslide.mpp-y')
    cfg['OnTheFly']['PixelSpacing'] = [float(x) for x in pv]

    return cfg
