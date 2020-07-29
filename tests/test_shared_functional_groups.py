#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import os
from yaml import load, BaseLoader, dump, FullLoader
from ..dicom_wsi.mods.parse_wsi import *
from ..dicom_wsi.mods.base_attributes import build_base
import datetime
from ..dicom_wsi.mods.sequence_attributes import build_sequences
from ..dicom_wsi.mods.shared_functional_groups import build_functional_groups

def test_get_wsi():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    base_yaml = os.path.join(dir_path,"base.yaml")
    # Load your YAML file
    cfg = load(open(base_yaml), Loader=BaseLoader)
    cfg, wsi = get_wsi(cfg)
    dict_dicom_returned = {}
    dcm, cfg = build_base(cfg, instance=3)
    dcm = build_sequences(dcm)
    dcm = build_functional_groups(dcm, cfg)

    dict_dicom_returned["ContentDate"]=dcm.ContentDate
    dict_dicom_returned["SOPInstanceUID"]=dcm.SOPInstanceUID
    dict_dicom_returned["SOPClassUID"]=dcm.SOPClassUID

    dict_dicom_expected = {}
    dict_dicom_expected["ContentDate"]=str(datetime.date.today()).replace('-', '')
    dict_dicom_expected["SOPInstanceUID"]='1.2.276.0.7230010.3.1.4.0.23267.1577648534.965883'
    dict_dicom_expected["SOPClassUID"]='1.2.840.10008.5.1.4.1.1.77.1.6'

    assert dict_dicom_returned == dict_dicom_expected





