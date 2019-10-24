import datetime
import logging
import random

import re

logger = logging.getLogger(__name__)


def add_data(ds, k, v):
    """
    :param ds: DICOM dataset
    :param k: DICOM keyword
    :param v: Value to set keyword
    :return:
    """
    logging.debug('Attempting to add ' + 'ds.' + str(k) + '=' + str(v))

    if isinstance(v, list):
        # Check to see if it is a string float or int
        try:
            tmp_var = str(int(v[0]))
            if v[0] == str(int(v[0])):
                # list_type = 'int'
                logger.debug('INT LIST: ds.' + k + ' = [' + ', '.join(x for x in v) + ']')
                exec('ds.' + k + ' = [' + ', '.join(x for x in v) + ']')
            else:
                # list_type = 'float'
                logger.debug('FLOAT LIST: ds.' + k + ' = [' + ', '.join(v) + ']')
                exec('ds.' + k + ' = [' + ', '.join(float(x) for x in v) + ']')
        except ValueError:
            # This is a string
            logger.debug('STR LIST: ds.' + k + ' = [' + ', '.join("'" + x + "'" for x in v) + ']')
            exec('ds.' + k + ' = [' + ', '.join("'" + x + "'" for x in v) + ']')
    else:
        logger.debug('V is not a list: {}\t{}'.format(k, v))
        cfg = None
        if re.match(re.compile("[a-zA-Z]"), str(v)):
            logger.debug('STR : ds.' + k + ' = ' + str(v))
            exec('ds.' + k + ' = ' + '\"' + str(v) + '\"')
        elif k.endswith('Date'):
            logger.debug('Date : ds.' + k + ' = ' + str(v))
            v = make_date(k, v, cfg, dict_element='utils')
            exec('ds.' + k + ' = ' + '\"' + str(v) + '\"')
        elif k.endswith('DateTime'):
            logger.debug('DATETIME : ds.' + k + ' = ' + str(v))
            v = make_datetime(k, v, cfg, dict_element='utils')
            exec('ds.' + k + ' = ' + '\"' + str(v) + '\"')
        elif k.endswith('Time') and not k.endswith('DateTime'):
            logger.debug('TIME : ds.' + k + ' = ' + str(v))
            v = make_time(k, v, cfg, dict_element='utils')
            exec('ds.' + k + ' = ' + '\"' + str(v) + '\"')
        # Account for UIDs
        elif k.endswith('UID'):
            logger.debug('UID: ds.' + k + ' = ' + str(v))
            exec('ds.' + k + ' = ' + '\"' + str(v) + '\"')
        elif v == int(v):
            # list_type = 'int'
            logger.debug('INT: ds.' + k + ' = ' + str(v))
            exec('ds.' + k + ' = ' + str(v))
        else:
            # list_type = 'float'
            logger.debug('FLOAT: ds.' + k + ' = ' + str(v))
            exec('ds.' + k + ' = ' + str(v))
    return ds


def uid_maker(k, v, cfg, dict_element='BaseAttributes'):
    if k == 'SOPClassUID' or k == 'SOPInstanceUID' or k == 'DimensionOrganizationUID':
        # These are all fixed values
        pass
    elif v.startswith('1.2'):
        # If user has already specificed a UID, use that
        pass
    else:
        r = random.randint(1, 100000)
        cfg[dict_element][k] = cfg['General']['OrgUIDRoot'] + '.' + str(r)
    return cfg[dict_element][k], cfg


def make_time(k, time_var, cfg, dict_element='BaseAttributes'):
    # Need to make sure it return the format HHMMSS.FFFFFF, or return a new one
    if re.match('\d\d\d\d\d\d\.\d\d\d\d\d\d', str(time_var)):
        # Already formatted properly
        t = datetime.time(int(time_var[:2]), int(time_var[2:4]), int(time_var[4:6]), int(time_var[8:]))
        time_var = t.strftime("%H%M%S.%f")
    elif re.match('\d\d:\d\d:\d\d', str(time_var)):
        h, m, s = time_var.split(':')
        t = datetime.time(int(h), int(m), int(s))
        time_var = t.strftime("%H%M%S.%f")
    else:
        raise ValueError('I do not know how to parse this format: {}'.format(time_var))

    if dict_element == 'utils':
        return time_var
    cfg[dict_element][k] = time_var
    return time_var, cfg


def make_datetime(k, datetime_var, cfg, dict_element='BaseAttributes'):
    # Need to make sure it return the format YYYYMMDDHHMMSS.FFFFFF, or return a new one
    if re.match('\d\d\d\d\d\d\d\d\d\d\d\d\d\d\.\d\d\d\d\d\d', str(datetime_var)):
        # Already formatted properly
        y = int(datetime_var[:4])
        m = int(datetime_var[4:6])
        d = int(datetime_var[6:8])
        H = int(datetime_var[8:10])
        M = int(datetime_var[10:12])
        S = int(datetime_var[12:14])
        F = int(datetime_var[16:])
        t = datetime.datetime(y, m, d, H, M, S, F)
        datetime_var = t.strftime("%Y%m%d%H%M%S.%f")
        logger.debug('FULL datetime_var: {}'.format(type(datetime_var)))
    elif re.match('\d\d:\d\d:\d\d', str(datetime_var)):
        h, m, s = datetime_var.split(':')
        t = datetime.time(int(h), int(m), int(s))
        datetime_var = t.strftime("%Y%m%d%H%M%S.%f")
        logger.debug('COLON datetime_var: {}'.format(type(datetime_var)))
    elif re.match('\d\d/\d\d/\d\d', str(datetime_var)):
        m, d, y = datetime_var.split('/')
        t = datetime.datetime(int(y), int(m), int(d))
        datetime_var = t.strftime("%Y%m%d%H%M%S.%f")
        logger.debug('SLASH datetime_var: {}'.format(type(datetime_var)))
    else:
        raise ValueError('I do not know how to parse this format: {}'.format(datetime_var))
    if dict_element == 'utils':
        return datetime_var
    cfg[dict_element][k] = datetime_var
    return datetime_var, cfg


def make_date(k, date_var, cfg, dict_element='BaseAttributes'):
    # Need to ensure date format returns properly, or return a new one
    if re.match('\d\d\d\d\d\d\d\d', str(date_var)):
        # Already formatted correctly
        date_var = datetime.datetime(int(date_var[0:4]), int(date_var[4:6]), int(date_var[7:])).strftime("%Y%m%d")
    elif re.match('\d\d/\d\d/\d\d', str(date_var)):
        m, d, y = date_var.split('/')
        date_var = datetime.datetime(int(y), int(m), int(d)).strftime("%Y%m%d")
    elif date_var is None or date_var == '000000.000000' or date_var == 'NUMBER':
        date_var = datetime.datetime.now().strftime("%Y%m%d")
    else:
        raise ValueError('I do not know how to parse this format: {}'.format(date_var))
    # Convert to string, since otherwise this crashes when writing DCM file
    date_var = str(date_var)
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
