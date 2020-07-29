#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import sys
import os

from yaml import load, BaseLoader, dump, FullLoader
from ..dicom_wsi.mods.parse_wsi import *
from ..dicom_wsi.mods.base_attributes import build_base
import datetime

def test_get_wsi():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    base_yaml = os.path.join(dir_path, "base.yaml")
    # Load your YAML file
    cfg = load(open(base_yaml), Loader=BaseLoader)
    cfg, wsi = get_wsi(cfg)
    dict_dicom_returned = {}
    dcm, cfg = build_base(cfg, instance=3)

    dict_dicom_returned["ContentDate"]=dcm.ContentDate
    dict_dicom_returned["SOPInstanceUID"]=dcm.SOPInstanceUID
    dict_dicom_returned["SOPClassUID"]=dcm.SOPClassUID
    dict_dicom_returned["StudyInstanceUID"]=dcm.StudyInstanceUID
    dict_dicom_returned["SeriesInstanceUID"]=dcm.SeriesInstanceUID
    dict_dicom_returned["PatientID"]=dcm.PatientID
    dict_dicom_expected = {}
    dict_dicom_expected["ContentDate"]=str(datetime.date.today()).replace('-', '')
    dict_dicom_expected["SOPInstanceUID"]='1.2.276.0.7230010.3.1.4.0.23267.1577648534.965883'
    dict_dicom_expected["StudyInstanceUID"]='1.2.276.0.7230010.3.1.2.0.23267.1577648488.965861'
    dict_dicom_expected["SeriesInstanceUID"]='1.2.276.0.7230010.3.1.3.0.23267.1577648488.965862'
    dict_dicom_expected["SOPClassUID"]='1.2.840.10008.5.1.4.1.1.77.1.6'
    dict_dicom_expected["PatientID"]='4f3a7f54-c23f-4d96-9a6c-35930bf6acc3'

    assert dict_dicom_returned == dict_dicom_expected

