import re

INT_LIST = ['DA', 'UL', 'US']
TIME_LIST = ['TM']
# noinspection SpellCheckingInspection
SIGNEDINT_LIST = ['US or SS']
# noinspection SpellCheckingInspection
INTSTRING_LIST = ['IS']
DT_LIST = ['DT']
DS_LIST = ['DS']
CS_LIST = ['CS']


def cs_validator(key, value):
    assert re.sub('[a-zA-Z _]', '', value).__len__() == 0, \
        "{} must only contain a-z, A-Z, space, or _, but your provided {}".format(key, value)


def int_validator(key, value):
    assert re.sub('[0-9]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, but your provided {}".format(key, value)


# noinspection SpellCheckingInspection
def signedint_validator(key, value):
    assert re.sub('[0-9-]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9 and -, but your provided {}".format(key, value)


def time_validator(key, value):
    assert re.sub('[0-9 .]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, space and ., but your provided {}".format(key, value)


def ui_validator(key, value):
    assert re.sub('[0-9.]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9 and ., but your provided {}".format(key, value)


def dt_validator(key, value):
    assert re.sub('[0-9+-. ]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, +, -, space, and ., but your provided {}".format(key, value)


def ds_validator(key, value):
    assert re.sub('[0-9+-eE]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, +, -, e, and E, but your provided {}".format(key, value)


# noinspection SpellCheckingInspection
def intstring_validator(key, value):
    assert re.sub('[0-9+-]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, +, and - but your provided {}".format(key, value)
