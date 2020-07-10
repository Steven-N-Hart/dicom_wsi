#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import os

from yaml import load, BaseLoader
from ..dicom_wsi.mods.parse_wsi import get_wsi
from ..dicom_wsi.mods.utils import make_time

def test_parse_wsi():
    base_yaml = os.path.join("dicom_wsi", "yaml", "base.yaml")

    # Load your YAML file
    cfg = load(open(base_yaml), Loader=BaseLoader)
    cfg['General']['WSIFile'] = os.path.join("tests", "CMU-1-JP2K-33005.svs")
    cfg, wsi = get_wsi(cfg)

