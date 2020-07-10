#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import os
from yaml import load, BaseLoader

from ..dicom_wsi.mods.parse_wsi import get_wsi
from ..dicom_wsi.mods.base_attributes import build_base
import datetime

def test_get_wsi():
    base_yaml = os.path.join("dicom_wsi", "yaml", "base.yaml")
    # Load your YAML file
    cfg = load(open(base_yaml), Loader=BaseLoader)
    cfg['WSIFile'] = os.path.join('tests','CMU-1-JP2K-33005.svs')
    try:
        cfg, wsi = get_wsi(cfg)
    except:
        print(f"unable to find {cfg['WSIFile']} in {os.getcwd()}")

    dcm, cfg = build_base(cfg, instance=3)
    assert dcm.ContentDate == str(datetime.date.today()).replace('-', '')
    assert dcm.SOPInstanceUID == '1.2.276.0.7230010.3.1.4.0.23267.1577648534.965883'
    assert dcm.SOPClassUID == '1.2.840.10008.5.1.4.1.1.77.1.6'
    assert dcm.StudyInstanceUID == '1.2.276.0.7230010.3.1.2.0.23267.1577648488.965861'
    assert dcm.SeriesInstanceUID == '1.2.276.0.7230010.3.1.3.0.23267.1577648488.965862'
    assert dcm.PatientID == '4f3a7f54-c23f-4d96-9a6c-35930bf6acc3'

if __name__ == '__main__':
    test_get_wsi()
