
def uid_maker(element_dict, uid='1.2.3.4'):
    # Need to better understand how to make uids
    return uid

def make_time(time_var):
    # Need to make sure it return the format HHMMSS.FFFFFF, or return a new one
    return time_var

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
