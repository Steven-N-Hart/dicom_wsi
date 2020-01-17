import utils


def map_aperio_features(cfg, wsi):
    """
    Update attributes by mapping from vendor specific attributes to DICOM attributes
    :param cfg:
    :param wsi:
    :return:
    """
    # TODO: Verify these are all getting added somewhere
    cfg['SharedFunctionalGroupsSequence'] = dict()  # TODO: not actually using this anywhere
    cfg['OnTheFly'] = dict()
    if not cfg.get('BaseAttributes').get('Manufacturer'):
        cfg['BaseAttributes']['Manufacturer'] = wsi.get('openslide.vendor')
    if not cfg.get('BaseAttributes').get('SeriesDescription'):
        cfg['BaseAttributes']['SeriesDescription'] = str(wsi.get('aperio.ImageID'))

    if not cfg.get('BaseAttributes').get('ContentTime'):
        _, cfg = utils.make_time('ContentTime', wsi.get('aperio.Time'), cfg,
                                 dict_element='SharedFunctionalGroupsSequence')
    else:
        cfg['SharedFunctionalGroupsSequence']['ContentTime'] = cfg['BaseAttributes']['ContentTime']

    if not cfg.get('BaseAttributes').get('SeriesTime'):
        _, cfg = utils.make_time('SeriesTime', wsi.get('aperio.Time'), cfg,
                                 dict_element='SharedFunctionalGroupsSequence')

    if not cfg.get('BaseAttributes').get('StudyTime'):
        _, cfg = utils.make_time('StudyTime', wsi.get('aperio.Time'), cfg,
                                 dict_element='SharedFunctionalGroupsSequence')
    else:
        cfg['SharedFunctionalGroupsSequence']['StudyTime'] = cfg['BaseAttributes']['StudyTime']

    pv = wsi.get('openslide.mpp-x'), wsi.get('openslide.mpp-y')
    cfg['OnTheFly']['PixelSpacing'] = [float(x) for x in pv]

    return cfg


