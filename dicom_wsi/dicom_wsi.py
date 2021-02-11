# -*- coding: utf-8 -*-
import logging

from .input_validation import validate_cfg
from .run import run_instance

logger = logging.getLogger(__name__)
import multiprocessing as mp

"""Main module."""


def create_dicom(cfg, pools=-1):
    """
    Main function for creating DICOM files
    :param cfg: dictionary containing all required variables
    :param pools: how many processors to use
    :return: 0
    """
    logger.debug('Beginning validation')
    validate_cfg(cfg)
    logger.info('All inputs are valid')
    number_of_levels = int(cfg.get('General').get('NumberOfLevels'))

    if pools < 0:
        pool = mp.Pool(mp.cpu_count())
        logger.debug(f'Using {mp.cpu_count()} CPUs')
    else:
        pool = mp.Pool(pools)
        logger.debug(f'Using {pools} CPUs')

    results = pool.starmap(run_instance, [(i, cfg) for i in reversed(range(number_of_levels))])
    pool.close()
