# -*- coding: utf-8 -*-

"""Console script for dicom_wsi."""
import argparse
import logging
import os
import sys

from . import parse_wsi
from yaml import load, BaseLoader

import dicom_wsi

def main():
    """Console script for dicom_wsi."""
    parser = argparse.ArgumentParser()

    parser.add_argument("-y", "--yaml",
                        dest='yaml',
                        required=True,
                        help="YAML file containing variables")

    parser.add_argument("-w", "--wsi",
                        dest='wsi',
                        help="Convenience function to override WSIFile value in yaml file")

    parser.add_argument("-o", "--outdir",
                        dest='out',
                        default='.',
                        help="Convenience function to override OutDir value in yaml file")

    parser.add_argument("-p", "--prefix",
                        dest='prefix',
                        default=None,
                        help="Convenience function to override OutFilePrefix value in yaml file")

    parser.add_argument("-t", "--tile_out",
                        dest='tile',
                        choices=['TILED_FULL', 'TILED_SPARSE'],
                        default='TILED_FULL',
                        help="Convenience function to override DimensionOrganizationType value in yaml file")

    parser.add_argument("-P", "--pools",
                        dest='pools',
                        default=-1,
                        help="How many CPUs to use (default=all")

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
    cfg, wsi = parse_wsi.get_wsi(cfg)

    if args.wsi:
        cfg['General']['WSIFile'] = args.wsi
        logging.debug(f'Overwriting WSIFile with : {args.wsi}')

    if args.out:
        cfg['General']['OutDir'] = args.out
        logging.debug(f'Overwriting OutDir with : {args.out}')

    if args.prefix:
        cfg['General']['OutFilePrefix'] = args.prefix
        logging.debug(f'Overwriting OutFilePrefix with : {args.prefix}')

    if args.tile:
        cfg['BaseAttributes']['DimensionOrganizationType'] = args.tile
        logging.debug(f'Overwriting DimensionOrganizationType with : {args.tile}')

    if not os.path.exists(cfg['General']['OutDir']):
        val = cfg['General']['OutDir']
        os.mkdir(val)
        logging.debug(f'Creating directory: {val}')

    # Combine the output directory and prefix so that the file can be written
    cfg['General']['OutFilePrefix'] = os.path.join(cfg['General']['OutDir'], cfg['General']['OutFilePrefix'])
    logging.debug(f'Running with parameters: {cfg}')

    dicom_wsi.create_dicom(cfg, pools=args.pools)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
