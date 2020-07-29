# -*- coding: utf-8 -*-
import logging
import sys
from mods.input_validation import validate_cfg
from mods.run import run_instance

logger = logging.getLogger(__name__)
import multiprocessing as mp

pool = mp.Pool(mp.cpu_count())

"""Main module."""



logger = logging.getLogger(__name__)
import multiprocessing as mp

pool = mp.Pool(mp.cpu_count())

"""Main module."""


def create_dicom(cfg):
    """
    Main function for creating DICOM files
    :param cfg: dictionary containing all required variables
    :return: 0
    """
    logger.debug('Beginning validation')
    validate_cfg(cfg)
    logger.info('All inputs are valid')
    number_of_levels = int(cfg.get('General').get('NumberOfLevels'))
    pool.starmap(run_instance, [(i, cfg) for i in reversed(range(number_of_levels))])
    pool.close()
