# -*- coding: utf-8 -*-
import os
import urllib.request

"""Unit test package for dicom_wsi."""
wsi_url = 'http://openslide.cs.cmu.edu/download/openslide-testdata/Aperio/CMU-1-JP2K-33005.svs'
if not os.path.exists(os.path.join('..', 'tests', 'CMU-1-JP2K-33005.svs')):
    urllib.request.urlretrieve(wsi_url, os.path.join('tests', 'CMU-1-JP2K-33005.svs'))
