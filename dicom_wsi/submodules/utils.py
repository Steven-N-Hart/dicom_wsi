import logging

for k, v in patient_dict.items():
def add_data(k, v):
    """

    :param k: DICOM keyword
    :param v: Value to set keyword
    :return:
    """
    logging.debug('Attempting to add ' + 'ds.' + str(k) + '=' + str(v))

    exec('ds.' + str(k) + '=\"' + str(v) + '\"')


def uid_maker(element_dict, uid='1.2.3.4'):
    # Need to better understand how to make uids
    return uid

def make_time(time_var):
    # Need to make sure it return the format HHMMSS.FFFFFF, or return a new one
    return time_var

def make_date(date_var):
    # Need to ensure date format returns properly, or return a new one
    return date_var
