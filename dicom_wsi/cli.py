# -*- coding: utf-8 -*-

"""Console script for dicom_wsi."""

import argparse
import logging
import sys

from yaml import load, BaseLoader

from dicom_wsi import create_dicom


def main():
    """Console script for dicom_wsi."""
    parser = argparse.ArgumentParser()

    parser.add_argument("-y", "--yaml",
                        dest='yaml',
                        help="YAML file containing variables")

    parser.add_argument("-V", "--verbose",
                        dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default="INFO",
                        help="Set the logging level")

    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=args.logLevel,
                        format='%(name)s (%(levelname)s): %(message)s')

    logger = logging.getLogger(__name__)
    logger.setLevel(args.logLevel)
    cfg = load(open(args.yaml), Loader=BaseLoader)
    create_dicom(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
