import submodules.character_validations as cv
import logging
logger = logging.getLogger(__name__)


def validate_cfg(cfg):
    """
    Validate the dictionary to make sure all the required elements are present
    :param cfg: a dictionary of values, separated by module name
    :return: 0
    """

    MODULES = ['General', 'Patient', 'Specimen', 'GeneralStudy', 'GeneralSeries', 'GeneralEquipment', 'EnhancedGeneralEquipment',
               'WholeSlideMicroscopyImage', 'AcquisitionContext', 'FrameOfReference', 'OpticalPath', 'SOPCommon',
               'ImagePixel', 'MultiFrameFunctionalGroups']
    for m in MODULES:
        try:
            _validate(m, cfg[m])
            logging.debug('{} data validated'.format(m))
        except KeyError:
            logging.debug('{} not found in your configuration.  Please define'.format(m))
            exit(1)

    logging.debug('All data validated')

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
        #logging.debug('Completed VR type validation for {}'.format(k))

        # Verify provided values are allowed
        if k in cv.restricted_inputs.keys():
            logging.debug('k {} is found in {}'.format(sample_dict[k], cv.restricted_inputs[k]))
            logging.debug('{}'.format(sample_dict))
            assert sample_dict[k] in cv.restricted_inputs[k], \
                'You provided {} for {}, but it only allows {}'.format(sample_dict[k], k, cv.restricted_inputs[k])
        logging.debug('Completed Allowed Values validation for {}'.format(k))

def _validate(module, sample_dict):
    required_keys = cv.required_fields[module]
    try:
        provided_keys = sample_dict.keys()
    except AttributeError:
        logging.debug('{} has no values, skipping'.format(module))
        return 0

    # Check to make sure an entry exists for all required fields
    for k in required_keys:
        assert k in provided_keys, 'You are missing the sample field for {}'.format(k)

    _validation_wrapper(provided_keys, sample_dict)
