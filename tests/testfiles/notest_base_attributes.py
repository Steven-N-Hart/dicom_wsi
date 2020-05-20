#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import sys
sys.path.append("../dicom_wsi/")
sys.path.append("../dicom_wsi/submodules")
#import pytest
from yaml import load, BaseLoader, dump
from base_attributes import build_base
import unittest

class TestBaseAttributesMethods(unittest.TestCase):
    def test_get_wsi(self):
        yaml = './testfiles/test_get_wsi.yaml'
        cfg	 = load(open(yaml), Loader=BaseLoader)
        number_of_levels = int(cfg.get('General').get('NumberOfLevels'))
        instance = 6
        dcm_returned, cfg_returned = build_base(cfg, instance=instance)
        yaml_ref = './testfiles/test_build_base.yaml'
        cfg_ref = load(open(yaml_ref), Loader=BaseLoader)
        # cfg_ref['BaseAttributes']['AcquisitionDateTime']['args'][0]='NA'
        # cfg_ref['BaseAttributes']['PatientBirthDate']['args'][0]='NA'
        # cfg_ref['BaseAttributes']['SeriesDate']['args'][0]='NA'
        # cfg_ref['BaseAttributes']['StudyDate']['args'][0]='NA'
        print(cfg_ref['BaseAttributes']['AcquisitionDateTime'])
        print(cfg_returned['BaseAttributes']['AcquisitionDateTime'])
        # sys.exit(0)
        # cfg_returned['BaseAttributes']['AcquisitionDateTime']['args'][0]='NA'
        # cfg_returned['BaseAttributes']['PatientBirthDate']['args'][0]='NA'
        # cfg_returned['BaseAttributes']['SeriesDate']['args'][0]='NA'
        # cfg_returned['BaseAttributes']['StudyDate']['args'][0]='NA'

        with open(r'Test1.yaml', 'w') as file:
            documents = dump(cfg_ref,file)
        with open(r'Test2.yaml', 'w') as file:
            documents = dump(cfg_returned,file)
        #for instance in reversed(range(number_of_levels)):
        #cfg_returned, wsi_returned = get_wsi(cfg)
        self.assertDictEqual(cfg_returned,cfg_ref)

 	
if __name__ == '__main__':
    unittest.main()
