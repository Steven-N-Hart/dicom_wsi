import datetime
import logging
import re

import pydicom
from pydicom.tag import Tag

logger = logging.getLogger(__name__)


def add_data(ds, k, v, cfg, dict_element=None):
    """
    Ensures the right kind of data is insreted into DICOM object (e.g. datetime, time, date, etc)

    :param ds: DICOM dataset
    :param k: DICOM keyword
    :param v: Value to set keyword
    :param cfg: config dict
    :param dict_element: which part of processing is this coming from
    :return:
    """
    logging.debug('Attempting to add ' + 'ds.' + str(k) + '=' + str(v))
    vr, vm = get_info_from_keyword(k)
    if vm > 1:
        if vr in ['DS', 'OF', 'FL', 'FD', 'OD']:
            v = [float(x) for x in v]
        elif vr in ['UL', 'US', 'SL', 'SS', 'IS']:
            v = [int(x) for x in v]
    else:
        logger.debug('V is not a list: {}\t{}'.format(k, v))
        if vr == 'DA':
            logger.debug('Date : ds.' + k + ' = ' + str(v))
            v, _ = make_date(k, v, cfg, dict_element=dict_element)
            ds.add_new(Tag(k), vr, v)
        elif vr == 'DT':
            logger.debug('DATETIME : ds.' + k + ' = ' + str(v))
            v, _ = make_datetime(k, v, cfg, dict_element=dict_element)
        elif vr == 'TM':
            logger.debug('TIME : ds.' + k + ' = ' + str(v))
            v, _ = make_time(k, v, cfg, dict_element=dict_element)
        # Account for UIDs
        elif vr == 'UI':
            logger.debug('UID: ds.' + k + ' = ' + str(v))
            v, _ = uid_maker(k, v, cfg, dict_element=dict_element)
        elif vr in ['UL', 'US', 'SL', 'SS', 'IS']:
            # list_type = 'int'
            v = int(v)
            logger.debug('INT: ds.' + k + ' = ' + str(v))
        elif vr in ['DS', 'OF', 'FL', 'FD', 'OD']:
            v = float(v)
            logger.debug('FLOAT: ds.' + k + ' = ' + str(v))
        elif vr in ['LO', 'LT', 'SH', 'ST', 'UT']:
            logger.debug('STR : ds.' + k + ' = ' + str(v))
        elif vr == 'PN':
            v = v.encode()

    ds.add_new(Tag(k), vr, v)

    return ds


def get_info_from_keyword(kw):
    # noinspection SpellCheckingInspection
    """
        Get Value data from Keywords

        :param kw: KeyWord
        :return: VR, VM, NAME, ISRETIRED, KW

        pydicom.datadict.get_entry('StudyDate')
        ('DA', '1', 'Study Date', '', 'StudyDate')
        """
    vr, vm, name, is_retired, ky_word = pydicom.datadict.get_entry(kw)
    try:
        vm = int(vm)
    except ValueError:
        vm = 2  # Change to > 1 so I can store multiple variables
    return vr, vm


# noinspection PyUnresolvedReferences
def uid_maker(k, v, cfg, dict_element='BaseAttributes'):
    """
    Make a UID if needed

    :param k: key
    :param v: value
    :param cfg: config file
    :param dict_element: which section/module the attributes belong to
    :return: updated config dictionary
    """
    if k == 'SOPClassUID' or k == 'SOPInstanceUID' or k == 'DimensionOrganizationUID':
        # These are all fixed values
        pass
    # elif k == 'SeriesInstanceUID':
    # Need to decrease the length of this UID because I append the series number to it
    #    cfg[dict_element][k] = pydicom.uid.generate_uid(prefix=cfg['General']['OrgUIDRoot'])[:60]
    elif v.startswith('1.2'):
        # If user has already specified a UID, use that
        pass
    else:
        cfg[dict_element][k] = pydicom.uid.generate_uid(prefix=cfg['General']['OrgUIDRoot'])
    return cfg[dict_element][k], cfg


# noinspection PyPep8,SpellCheckingInspection
def make_time(k, time_var, cfg, dict_element='BaseAttributes'):
    """
    Need to make sure it return the format HHMMSS.FFFFFF, or return a new one

    :param k: key
    :param time_var: value
    :param cfg: config file
    :param dict_element: which section/module the attributes belong to
    :return: updated config dictionary
    """
    # Need to make sure it return the format HHMMSS.FFFFFF, or return a new one
    if isinstance(time_var, datetime.time):
        pass
    elif re.match(r'\d\d\d\d\d\d\.\d\d\d\d\d\d', str(time_var)):
        # Already formatted properly
        t = datetime.time(int(time_var[:2]), int(time_var[2:4]), int(time_var[4:6]), int(time_var[8:]))
        time_var = t.strftime("%H%M%S.%f")
    elif re.match(r'\d\d:\d\d:\d\d', str(time_var)):
        h, m, s = time_var.split(':')
        t = datetime.time(int(h), int(m), int(s))
        time_var = t.strftime("%H%M%S.%f")
    elif re.match(r'\d\d/\d\d/\d\d', str(time_var)):
        h, m, s = time_var.split('/')
        t = datetime.time(int(h), int(m), int(s))
        time_var = t.strftime("%H%M%S.%f")
    else:
        raise ValueError('I do not know how to parse this format: {}'.format(time_var))
    time_var = pydicom.valuerep.TM(time_var)
    if dict_element == 'utils':
        return time_var
    cfg[dict_element][k] = time_var
    return time_var, cfg


# noinspection PyPep8Naming,PyPep8,SpellCheckingInspection
def make_datetime(k, datetime_var, cfg, dict_element='BaseAttributes'):
    """
    Need to make sure it return the format YYYYMMDDHHMMSS.FFFFFF, or return a new one

    :param k: key
    :param datetime_var: value
    :param cfg: config file
    :param dict_element: which section/module the attributes belong to
    :return: updated config dictionary
    """
    # Need to make sure it return the format YYYYMMDDHHMMSS.FFFFFF, or return a new one
    if isinstance(datetime_var, datetime.datetime):
        pass
    elif re.match(r'\d\d\d\d\d\d\d\d\d\d\d\d\d\d\.\d\d\d\d\d\d', str(datetime_var)):
        # Already formatted properly
        y = int(datetime_var[:4])
        m = int(datetime_var[4:6])
        d = int(datetime_var[6:8])
        # noinspection PyPep8Naming
        H = int(datetime_var[8:10])
        M = int(datetime_var[10:12])
        S = int(datetime_var[12:14])
        F = int(datetime_var[16:])
        t = datetime.datetime(y, m, d, H, M, S, F)
        datetime_var = t.strftime("%Y%m%d%H%M%S.%f")
        datetime_var = pydicom.valuerep.DT(datetime_var)
        logger.debug('FULL datetime_var: {}'.format(type(datetime_var)))
    elif re.match(r'\d\d:\d\d:\d\d', str(datetime_var)):
        h, m, s = datetime_var.split(':')
        t = datetime.time(int(h), int(m), int(s))
        datetime_var = t.strftime("%Y%m%d%H%M%S.%f")
        datetime_var = pydicom.valuerep.DT(datetime_var)
        logger.debug('COLON datetime_var: {}'.format(type(datetime_var)))
    elif re.match(r'\d\d/\d\d/\d\d', str(datetime_var)):
        m, d, y = datetime_var.split('/')
        t = datetime.datetime(int(y), int(m), int(d))
        datetime_var = t.strftime("%Y%m%d%H%M%S.%f")
        datetime_var = pydicom.valuerep.DT(datetime_var)
        logger.debug('SLASH datetime_var: {}'.format(type(datetime_var)))
    else:
        raise ValueError('I do not know how to parse this format: {}'.format(datetime_var))
    if dict_element == 'utils':
        return datetime_var
    cfg[dict_element][k] = datetime_var
    return datetime_var, cfg


# noinspection PyPep8
def make_date(k, date_var, cfg, dict_element='BaseAttributes'):
    """
    Need to make sure it return the format YYYYMMDD, or return a new one

    :param k: key
    :param date_var: value
    :param cfg: config file
    :param dict_element: which section/module the attributes belong to
    :return: updated config dictionary
    """
    if isinstance(date_var, datetime.date):
        pass
    # Need to ensure date format returns properly, or return a new one
    elif re.match(r'\d\d\d\d\d\d\d\d', str(date_var)):
        # Already formatted correctly
        date_var = datetime.datetime(int(date_var[0:4]), int(date_var[4:6]), int(date_var[6:])).strftime("%Y%m%d")
    elif re.match(r'\d\d/\d\d/\d\d', str(date_var)):
        m, d, y = date_var.split('/')
        date_var = datetime.datetime(int(y), int(m), int(d)).strftime("%Y%m%d")
    elif date_var is None or date_var == '000000.000000' or date_var == 'NUMBER':
        date_var = datetime.datetime.now().strftime("%Y%m%d")

    else:
        raise ValueError('I do not know how to parse this format: {}'.format(date_var))
    # Convert to string, since otherwise this crashes when writing DCM file
    date_var = pydicom.valuerep.DA(date_var)
    if dict_element == 'utils':
        return date_var
    cfg[dict_element][k] = date_var

    return date_var, cfg


def get_all_keys(d, prefix=False):
    """
    Return a list of all keys (even nested ones from dict

    :param d: nested dictionary
    :param prefix: Whether or not to provide dot notation to keep the nesting information

    :return: list of keys
    """
    key_list = list()

    for k in d.keys():
        try:
            key_list.append(k)
            for l in d[k].keys():
                try:
                    key_list.append(l)
                    for m in d[k][l].keys():
                        if prefix is True:
                            key_list.append(k + '.' + l + '.' + m)
                        else:
                            key_list.append(m)
                except AttributeError:
                    if prefix is True:
                        key_list.append(k + '.' + l)
                    else:
                        key_list.append(l)
        except AttributeError:
            key_list.append(k)

    return key_list
