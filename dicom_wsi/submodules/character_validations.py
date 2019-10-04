import re

def cs_validator(key, value):
    assert re.sub('[a-zA-Z _]', '', value).__len__() == 0, \
        "{} must only contain a-z, A-Z, space, or _, but your provided {}".format(key, value)

def int_validator(key, value):
    assert re.sub('[0-9]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, but your provided {}".format(key, value)

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
