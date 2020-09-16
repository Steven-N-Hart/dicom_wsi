#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import json
import os

from yaml import load, BaseLoader


# class TestParseWSIMethods(unittest.TestCase):
def test_get_wsi():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    base_yaml = os.path.join(dir_path, "base.yaml")
    # Load your YAML file
    cfg = load(open(base_yaml), Loader=BaseLoader)

    wsi_fn_retuned = cfg.get('General')
    wsi_fn_expected = {'WSIFile': 'tests/CMU-1-JP2K-33005.svs', 'OutFilePrefix': './tests/output',
                       'NumberOfLevels': '7', 'OrgUIDRoot': '1.2.840.113713.15.',
                       'FrameSize': '500', 'MaxFrames': '500', 'ImageFormat': '.jpg', 'CompressionAmount': '90',
                       'background_range': '80', 'threshold': '0.5', 'Annotations': './tests/CMU-1-JP2K-33005.xml'}
    dict_wsi_fn_retuned = json.dumps(wsi_fn_retuned, sort_keys=True)
    dict_wsi_fn_expected = json.dumps(wsi_fn_expected, sort_keys=True)
    assert dict_wsi_fn_retuned == dict_wsi_fn_expected
