import logging

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
    return time_var

def make_datetime(datetime_var):
    # Need to make sure it return the format YYYYMMDDHHMMSS.FFFFFF, or return a new one
    return datetime_var

def make_date(date_var):
    # Need to ensure date format returns properly, or return a new one
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
