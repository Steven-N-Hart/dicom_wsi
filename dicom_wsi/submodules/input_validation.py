import submodules.character_validations as cv
import logging
logger = logging.getLogger('wsi_dicom_logger')

def validate_cfg(cfg):
    """
    Validate the dictionary to make sure all the required elements are present
    :param cfg: a dictionary of values, separated by module name
    :return: 0
    """
    print(cfg)
    _validate_sample(cfg['Patient'])

def _validation_wrapper(provided_keys, sample_dict):
    for k in provided_keys:
        if k in cv.CS_LIST:
            cv.cs_validator(k, sample_dict[k])
        elif k in cv.DS_LIST:
            cv.ds_validator(k, sample_dict[k])
        elif k in cv.INT_LIST:
            cv.int_validator(k, sample_dict[k])
        elif k in cv.TIME_LIST:
            cv.time_validator(k, sample_dict[k])
        elif k in cv.SIGNEDINT_LIST:
            cv.signedint_validator(k, sample_dict[k])
        elif k in cv.DT_LIST:
            cv.dt_validator(k, sample_dict[k])
        elif k in cv.INTSTRING_LIST:
            cv.intstring_validator(k, sample_dict[k])
        pass


def _validate_sample(sample_dict):
    required_keys = ['PatientName', 'PatientSex']
    provided_keys = sample_dict.keys()

    for k in required_keys:
        assert k in provided_keys, 'You are missing the sample field for {}'.format(k)

    _validation_wrapper(provided_keys, sample_dict)
    logging.info('Sample data valid')
