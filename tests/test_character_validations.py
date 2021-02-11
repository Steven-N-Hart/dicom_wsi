#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dicom_wsi` package."""
import pytest
from ..dicom_wsi import character_validations as cv


def test_cs():
    cv.cs_validator('patient', 'Roberto')
    with pytest.raises(AssertionError):
        cv.cs_validator('patient', 'Roberto#')


def test_int_validator():
    cv.int_validator('date', 20190304)
    cv.int_validator('date', '20190304')
    with pytest.raises(AssertionError):
        cv.int_validator('date', '20190304x')


def test_signedint_validator():
    cv.signedint_validator('Pixel padding value', '-001102')
    with pytest.raises(AssertionError):
        cv.signedint_validator('Pixel padding value', '-001102 ')


def test_time_validator():
    cv.time_validator('date', '201901.121 ')
    with pytest.raises(AssertionError):
        cv.time_validator('date', '2019/01/01')


def test_ui_validator():
    cv.ui_validator('UID', '201901.121')
    with pytest.raises(AssertionError):
        cv.ui_validator('UID', '2019/01/01')


def test_dt_validator():
    cv.dt_validator('datetime', '2019.+-')
    with pytest.raises(AssertionError):
        cv.dt_validator('datetime', 'q 2019.+-')


def test_ds_validator():
    cv.ds_validator('Xoffset', '+2.3e6')
    cv.ds_validator('Xoffset', '-2.3E6')
    cv.ds_validator('Xoffset', '230000000')
    with pytest.raises(AssertionError):
        cv.ds_validator('Xoffset', '2.3**6')
        cv.ds_validator('Xoffset', '2.3^6')


def test_intstring_validator():
    cv.intstring_validator('Series Number', '+30000')
    with pytest.raises(AssertionError):
        cv.int_validator('SER', 'a')


