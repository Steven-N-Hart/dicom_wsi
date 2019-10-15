import datetime
import logging
import re


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
                logging.debug('INT LIST: ds.' + k + ' = [' + ', '.join(x for x in v) + ']')
                exec('ds.' + k + ' = [' + ', '.join(x for x in v) + ']')
            else:
                #list_type = 'float'
                logging.debug('FLOAT LIST: ds.' + k + ' = [' + ', '.join(v) + ']')
                exec('ds.' + k + ' = [' + ', '.join(float(x) for x in v) + ']')
        except ValueError:
            # This is a string
            logging.debug('STR LIST: ds.' + k + ' = [' + ', '.join("'" + x + "'" for x in v) + ']')
            exec('ds.' + k + ' = [' + ', '.join("'" + x + "'" for x in v) + ']')
    else:
        exec('ds.' + str(k) + '=\"' + str(v) + '\"')
    logging.debug('Completed' + 'ds.' + str(k) + '=' + str(v))
    return ds


def uid_maker(element_dict, uid='1.2.3.4'):
    # Need to better understand how to make uids
    return uid

def make_time(time_var):
    # Need to make sure it return the format HHMMSS.FFFFFF, or return a new one
    if re.match('\d\d\d\d\d\d\.\d\d\d\d\d\d', time_var):
        # Already formatted properly
        pass
    elif re.match('\d\d:\d\d:\d\d', time_var):
        h, m, s = time_var.split(':')
        t = datetime.time(int(h), int(m), int(s))
        time_var = t.strftime("%H%M%S.%f")
    else:
        raise ValueError('I do not know how to parse this format: {}'.format(time_var))
    return time_var

def make_datetime(datetime_var):
    # Need to make sure it return the format YYYYMMDDHHMMSS.FFFFFF, or return a new one
    if re.match('\d\d\d\d\d\d\d\d\d\d\d\d\d\d\.\d\d\d\d\d\d', datetime_var):
        # Already formatted properly
        pass
    elif re.match('\d\d:\d\d:\d\d', datetime_var):
        h, m, s = datetime_var.split(':')
        t = datetime.time(int(h), int(m), int(s))
        datetime_var = t.strftime("%Y%m%d%H%M%S.%f")
    elif re.match('\d\d/\d\d/\d\d', datetime_var):
        m, d, y = datetime_var.split('/')
        datetime_var = datetime.datetime(int(y), int(m), int(d)).strftime("%Y%m%d%H%M%S.%f")
    else:
        raise ValueError('I do not know how to parse this format: {}'.format(datetime_var))
    return datetime_var

def make_date(date_var):
    # Need to ensure date format returns properly, or return a new one
    if re.match('\d\d\d\d\d\d', date_var):
        # Already formatted correctly
        pass
    if re.match('\d\d/\d\d/\d\d', date_var):
        m, d, y = date_var.split('/')
        date_var = datetime.datetime(int(y), int(m), int(d)).strftime("%Y%m%d")
    elif date_var is None or date_var == '000000.000000' or date_var == 'NUMBER':
        date_var = datetime.datetime.now().strftime("%Y%m%d")
    else:
        raise ValueError('I do not know how to parse this format: {}'.format(date_var))
    return date_var


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
