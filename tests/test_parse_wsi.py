#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import sys, os
#sys.path.append("../dicom_wsi/")
#sys.path.append("../dicom_wsi/submodules")
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from yaml import load, BaseLoader, dump, FullLoader
from ..dicom_wsi.mods import parse_wsi
from ..dicom_wsi.mods.parse_wsi import *
#import unittest
import json

#class TestParseWSIMethods(unittest.TestCase):
def test_get_wsi():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    base_yaml = os.path.join(dir_path,"base.yaml")
    # Load your YAML file
    cfg = load(open(base_yaml), Loader=BaseLoader)

    wsi_fn_retuned = cfg.get('General')
    wsi_fn_expected = {'WSIFile': './tests/CMU-1-JP2K-33005.svs', 'OutFilePrefix': './tests/output', 'NumberOfLevels': '7', 'OrgUIDRoot': '1.2.840.113713.15.', 'WSIBrand': 'aperio_svs', 'FrameSize': '500', 'MaxFrames': '500', 'ImageFormat': '.jpg', 'CompressionAmount': '90', 'background_range': '80', 'threshold': '0.5', 'Annotations': './tests/CMU-1-JP2K-33005.xml'}
    dict_wsi_fn_retuned = json.dumps(wsi_fn_retuned, sort_keys=True)
    dict_wsi_fn_expected = json.dumps(wsi_fn_expected, sort_keys=True)
    assert dict_wsi_fn_retuned == dict_wsi_fn_expected

