import logging
from datetime import datetime
import pyvips
from . import utils

logger = logging.getLogger(__name__)


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


def map_other_features(cfg, wsi):
    """
    Update attributes by mapping from vendor specific attributes to DICOM attributes
    :param cfg:
    :param wsi:
    :return:
    """
    fields = wsi.get_fields()
    cfg['OnTheFly'] = dict()
    logger.debug(f'Looking through fields:{fields}')
    if not cfg.get('BaseAttributes').get('Manufacturer'):
        cfg['BaseAttributes']['Manufacturer'] = wsi.get('openslide.vendor')

    if not cfg.get('BaseAttributes').get('SeriesDescription'):
        try:
            target = [field for field in fields if "ImageID" in field][0]
            cfg['BaseAttributes']['SeriesDescription'] = str(wsi.get(target))
        except:
            logging.warning(f'SeriesDescription not provided')
            cfg['BaseAttributes']['SeriesDescription'] = 'No description provided'

    if not cfg.get('BaseAttributes').get('ContentTime'):
        _, cfg = utils.make_time('ContentTime', wsi.get('aperio.Time'), cfg,
                                 dict_element='SharedFunctionalGroupsSequence')

    try:
        target = [field for field in fields if "Time" in field][0]
        logger.debug(f'Found target: {target}')
        if not cfg.get('BaseAttributes').get('SeriesTime'):
            _, cfg = utils.make_time('SeriesTime', wsi.get(target), cfg,
                                     dict_element='SharedFunctionalGroupsSequence')

        if not cfg.get('BaseAttributes').get('StudyTime'):
            _, cfg = utils.make_time('StudyTime', wsi.get(target), cfg,
                                     dict_element='SharedFunctionalGroupsSequence')
        if not cfg.get('BaseAttributes').get('ContentTime'):
            _, cfg = utils.make_time('ContentTime', wsi.get(target), cfg,
                                     dict_element='SharedFunctionalGroupsSequence')

    except IndexError:
        now = datetime.now().strftime("%H%M%S.%f")
        logging.warning(f'Unable to find StudyTime/SeriesTime. Using datenow({now}) instead')
        if not cfg.get('BaseAttributes').get('StudyTime'):
            _, cfg = utils.make_time('StudyTime', now, cfg,
                                     dict_element='SharedFunctionalGroupsSequence')
        if not cfg.get('BaseAttributes').get('SeriesTime'):
            _, cfg = utils.make_time('SeriesTime', now, cfg,
                                     dict_element='SharedFunctionalGroupsSequence')
        if not cfg.get('BaseAttributes').get('ContentTime'):
            _, cfg = utils.make_time('ContentTime', now, cfg,
                                     dict_element='SharedFunctionalGroupsSequence')

    try:
        pv = wsi.get('openslide.mpp-x'), wsi.get('openslide.mpp-y')
    except pyvips.error.Error:
        try:
            logger.warning('openslide.mpp-? not found. trying config file')
            pv = cfg.get('BaseAttributes').get('PixelSpacing')
            logger.warning(f'PV: {pv}')
        except:
            logger.error('openslide.mpp-? not found in config file or image file')
            raise AttributeError("openslide.mpp-? not found. You need to specify these values in your"
                                 " base.yaml: BaseAttributes.PixelSpacing: x,y")
    cfg['OnTheFly']['PixelSpacing'] = [float(x) for x in pv]

    return cfg
