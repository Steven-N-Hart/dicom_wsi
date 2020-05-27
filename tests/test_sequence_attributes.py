#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import sys
import os 
#sys.path.append("../dicom_wsi/")
#sys.path.append("../dicom_wsi/submodules")
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from yaml import load, BaseLoader, dump, FullLoader
from ..dicom_wsi.mods import parse_wsi
from ..dicom_wsi.mods.parse_wsi import *
#import unittest
import json
from ..dicom_wsi.mods.base_attributes import build_base
import datetime
from ..dicom_wsi.mods.sequence_attributes import build_sequences
#class TestParseWSIMethods(unittest.TestCase):
def test_get_wsi():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    base_yaml = os.path.join(dir_path,"testfiles","base.yaml")
    # Load your YAML file
    cfg = load(open(base_yaml), Loader=BaseLoader)
    cfg, wsi = get_wsi(cfg)
    #print(cfg['BaseAttributes']['SeriesInstanceUID'])
    dict_dicom_expected = {}
    dict_dicom_returned = {}
    dcm, cfg = build_base(cfg, instance=3)
    
    #print(dcm.SeriesInstanceUID)
    dcm = build_sequences(dcm)
    #print(dcm.SeriesInstanceUID)
    #print(dcm)
    #sys.exit(0)
    dict_dicom_returned["ContentDate"]=dcm.ContentDate
    dict_dicom_returned["SOPInstanceUID"]=dcm.SOPInstanceUID
    dict_dicom_returned["SOPClassUID"]=dcm.SOPClassUID
    
    dict_dicom_expected = {}
    dict_dicom_expected["ContentDate"]=str(datetime.date.today()).replace('-', '')
    dict_dicom_expected["SOPInstanceUID"]='1.2.276.0.7230010.3.1.4.0.23267.1577648534.965883'
    dict_dicom_expected["SOPClassUID"]='1.2.840.10008.5.1.4.1.1.77.1.6'
    
    #print(dict_dicom_returned,dict_dicom_expected)
    #sys.exit(0)
    assert dict_dicom_returned == dict_dicom_expected

# (0008, 0100) Code Value                          SH: '111609'
# (0008, 0100) Code Value                          SH: '111744'
# (0008, 0102) Coding Scheme Designator            SH: 'DCM'
# (0008, 0104) Code Meaning                        LO: 'Brightfield illumination'
# (0008, 0104) Code Meaning                        LO: 'No filter'
# (0020, 9164) Dimension Organization UID          UI: 1.2.276.0.7230010.3.1.4.8323329.20175.1573232544.237437
# (0020, 9165) Dimension Index Pointer             AT: (0048, 021e)
# (0020, 9165) Dimension Index Pointer             AT: (0048, 021f)
# (0020, 9167) Functional Group Pointer            AT: (0048, 021a)
# (0020, 9221)  Dimension Organization Sequence   1 item(s) ----
# (0020, 9222)  Dimension Index Sequence   2 item(s) ----
# (0022, 0016)  Illumination Type Code Sequence   1 item(s) ----
# (0028, 2000) ICC Profile                         OB: Array of 6922 elements
# (0040, 0031) Local Namespace Entity ID           UT: 'UNKNOWN'
# (0040, 0512) Container Identifier                LO: 'UNKNOWN'
# (0040, 0513)  Issuer of the Container Identifier Sequence   1 item(s) ----
# (0040, 0518)  Container Type Code Sequence   0 item(s) ----
# (0040, 0551) Specimen Identifier                 LO: 'UNKNOWN'
# (0040, 0554) Specimen UID                        UI: 2.25.45173726398442198918280102414634827093
# (0040, 0555)  Acquisition Context Sequence   0 item(s) ----
# (0040, 0560)  Specimen Description Sequence   1 item(s) ----
# (0040, 0562)  Issuer of the Specimen Identifier Sequence   0 item(s) ----
# (0040, 0610)  Specimen Preparation Sequence   0 item(s) ----
# (0040, 072a) X Offset in Slide Coordinate System DS: "20.0"
# (0040, 073a) Y Offset in Slide Coordinate System DS: "40.0"
# (0048, 0008)  Total Pixel Matrix Origin Sequence   1 item(s) ----
# (0048, 0105)  Optical Path Sequence   1 item(s) ----
# (0048, 0106) Optical Path Identifier             SH: '1'
# (0048, 0107) Optical Path Description            ST: 'Brightfield'
# (0048, 0108)  Illumination Color Code Sequence   1 item(s) ----



# (0008, 0005) Specific Character Set              CS: 'ISO_IR 100'
# (0008, 0008) Image Type                          CS: ['ORIGINAL', 'PRIMARY', 'VOLUME', 'NONE']
# (0008, 0016) SOP Class UID                       UI: VL Whole Slide Microscopy Image Storage
# (0008, 0018) SOP Instance UID                    UI: 1.2.276.0.7230010.3.1.4.0.23267.1577648534.965883
# (0008, 0020) Study Date                          DA: "20191229"
# (0008, 0021) Series Date                         DA: "20191229"
# (0008, 0023) Content Date                        DA: '20200515'
# (0008, 002a) Acquisition DateTime                DT: "20191229194128.000000"
# (0008, 0030) Study Time                          TM: "194128.000000"
# (0008, 0031) Series Time                         TM: "194128.000000"
# (0008, 0033) Content Time                        TM: "194128.000000"
# (0008, 0050) Accession Number                    SH: 'UNKNOWN'
# (0008, 0060) Modality                            CS: 'SM'
# (0008, 0070) Manufacturer                        LO: 'aperio'
# (0008, 0090) Referring Physician's Name          PN: 'UNKNOWN^UNKNOWN'
# (0008, 103e) Series Description                  LO: '1004486'
# (0008, 1090) Manufacturer's Model Name           LO: 'UNKNOWN'
# (0008, 9206) Volumetric Properties               CS: 'VOLUME'
# (0010, 0010) Patient's Name                      PN: 'Bo^Jangles'
# (0010, 0020) Patient ID                          LO: '4f3a7f54-c23f-4d96-9a6c-35930bf6acc3'
# (0010, 0030) Patient's Birth Date                DA: "20000101"
# (0010, 0040) Patient's Sex                       CS: 'M'
# (0018, 1000) Device Serial Number                LO: 'UNKNOWN'
# (0018, 1020) Software Versions                   LO: 'UNKNOWN'
# (0020, 000d) Study Instance UID                  UI: 1.2.276.0.7230010.3.1.2.0.23267.1577648488.965861
# (0020, 000e) Series Instance UID                 UI: 1.2.276.0.7230010.3.1.3.0.23267.1577648488.965862
# (0020, 0010) Study ID                            SH: 'Test'
# (0020, 0020) Patient Orientation                 CS: ''
# (0020, 9221)  Dimension Organization Sequence   1 item(s) ----
# (0020, 9164) Dimension Organization UID          UI: 1.2.276.0.7230010.3.1.4.8323329.20175.1573232544.237437
# ---------
# (0020, 9222)  Dimension Index Sequence   2 item(s) ----
# (0020, 9164) Dimension Organization UID          UI: 1.2.276.0.7230010.3.1.4.8323329.20175.1573232544.237437
# (0020, 9165) Dimension Index Pointer             AT: (0048, 021e)
# (0020, 9167) Functional Group Pointer            AT: (0048, 021a)
# ---------
# (0020, 9164) Dimension Organization UID          UI: 1.2.276.0.7230010.3.1.4.8323329.20175.1573232544.237437
# (0020, 9165) Dimension Index Pointer             AT: (0048, 021f)
# (0020, 9167) Functional Group Pointer            AT: (0048, 021a)
# ---------
# (0020, 9311) Dimension Organization Type         CS: 'TILED_SPARSE'
# (0028, 0002) Samples per Pixel                   US: 3
# (0028, 0004) Photometric Interpretation          CS: 'RGB'
# (0028, 0006) Planar Configuration                US: 0
# (0028, 0100) Bits Allocated                      US: 8
# (0028, 0101) Bits Stored                         US: 8
# (0028, 0102) High Bit                            US: 7
# (0028, 0103) Pixel Representation                US: 0
# (0028, 0301) Burned In Annotation                CS: 'NO'
# (0040, 0512) Container Identifier                LO: 'UNKNOWN'
# (0040, 0513)  Issuer of the Container Identifier Sequence   1 item(s) ----
# (0040, 0031) Local Namespace Entity ID           UT: 'UNKNOWN'
# ---------
# (0040, 0518)  Container Type Code Sequence   0 item(s) ----
# (0040, 0555)  Acquisition Context Sequence   0 item(s) ----
# (0040, 0560)  Specimen Description Sequence   1 item(s) ----
# (0040, 0551) Specimen Identifier                 LO: 'UNKNOWN'
# (0040, 0554) Specimen UID                        UI: 2.25.45173726398442198918280102414634827093
# (0040, 0562)  Issuer of the Specimen Identifier Sequence   0 item(s) ----
# (0040, 0610)  Specimen Preparation Sequence   0 item(s) ----
# ---------
# (0048, 0001) Imaged Volume Width                 FL: 15.0
# (0048, 0002) Imaged Volume Height                FL: 15.0
# (0048, 0003) Imaged Volume Depth                 FL: 1.0
# (0048, 0008)  Total Pixel Matrix Origin Sequence   1 item(s) ----
# (0040, 072a) X Offset in Slide Coordinate System DS: "20.0"
# (0040, 073a) Y Offset in Slide Coordinate System DS: "40.0"
# ---------
# (0048, 0010) Specimen Label in Image             CS: 'NO'
# (0048, 0011) Focus Method                        CS: 'AUTO'
# (0048, 0012) Extended Depth of Field             CS: 'NO'
# (0048, 0102) Image Orientation (Slide)           DS: [0.0, -1.0, 0.0, -1.0, 0.0, 0.0]
# (0048, 0105)  Optical Path Sequence   1 item(s) ----
# (0022, 0016)  Illumination Type Code Sequence   1 item(s) ----
# (0008, 0100) Code Value                          SH: '111744'
# (0008, 0102) Coding Scheme Designator            SH: 'DCM'
# (0008, 0104) Code Meaning                        LO: 'Brightfield illumination'
# ---------
# (0028, 2000) ICC Profile                         OB: Array of 6922 elements
# (0048, 0106) Optical Path Identifier             SH: '1'
# (0048, 0107) Optical Path Description            ST: 'Brightfield'
# (0048, 0108)  Illumination Color Code Sequence   1 item(s) ----
# (0008, 0100) Code Value                          SH: '111609'
# (0008, 0102) Coding Scheme Designator            SH: 'DCM'
# (0008, 0104) Code Meaning                        LO: 'No filter'
# ---------
# ---------
# (0048, 0302) Number of Optical Paths             UL: 1
# (0048, 0303) Total Pixel Matrix Focal Planes     UL: 1
