# !/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright © 2019 Koninklijke Philips N.V. All Rights Reserved.

# A copyright license is hereby granted for redistribution and use of the
# Software in source and binary forms, with or without modification, provided
# that the following conditions are met:
# • Redistributions of source code must retain the above copyright notice, this
#   copyright license and the following disclaimer.
# • Redistributions in binary form must reproduce the above copyright notice,
#   this copyright license and the following disclaimer in the documentation
#   and/ or other materials provided with the distribution.
# • Neither the name of Koninklijke Philips N.V. nor the names of its
#   subsidiaries may be used to endorse or promote products derived from the
#   Software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

"""
libTIFF interfacing code
"""

import ctypes
import platform
import sys

# Specify the path for the lib tiff dll
# Change this path according to your Operating System(OS)
if "win" in sys.platform:
    LIBTIFF = ctypes.cdll.LoadLibrary(r'libtiff-5.dll')
elif "Ubuntu" in platform.linux_distribution()[0]:
    LIBTIFF = ctypes.cdll.LoadLibrary(r'/usr/lib/x86_64-linux-gnu/libtiff.so')
if LIBTIFF is None:
    raise TypeError('Failed to load libtiff')

# TIFFTAG_* constants from the header file:
TIFFTAG_IMAGEWIDTH = 256
TIFFTAG_IMAGELENGTH = 257
TIFFTAG_TILEWIDTH = 322
TIFFTAG_TILELENGTH = 323
TIFFTAG_BITSPERSAMPLE = 258
TIFFTAG_COMPRESSION = 259
COMPRESSION_JPEG = 7
TIFFTAG_SAMPLESPERPIXEL = 277
TIFFTAG_PLANARCONFIG = 284
TIFFTAG_PHOTOMETRIC = 262
TIFFTAG_JPEGQUALITY = 65537
TIFFTAG_ORIENTATION = 274
ORIENTATION_TOPLEFT = 1
TIFFTAG_JPEGCOLORMODE = 65538
JPEGCOLORMODE_RGB = 1
TIFFTAG_SUBFILETYPE = 254
PHOTOMETRIC_RGB = 2
PHOTOMETRIC_YCBCR = 6
FILETYPE_REDUCEDIMAGE = 0x1
TIFFTAG_YCBCRSUBSAMPLING = 530
BITSPERSAMPLE = 8
SAMPLESPERPIXEL = 3
PLANARCONFIG = 1
JPEGQUALITY = 80
YCBCRHORIZONTAL = 2
YCBCRVERTICAL = 2
TIFF_TILE_WIDTH = 512
TIFF_TILE_HEIGHT = 512

TIFFTAGS = {
    TIFFTAG_IMAGEWIDTH: (ctypes.c_uint32, lambda _d: _d.value),
    TIFFTAG_IMAGELENGTH: (ctypes.c_uint32, lambda _d: _d.value),
    TIFFTAG_SAMPLESPERPIXEL: (ctypes.c_uint32, lambda _d: _d.value),
    TIFFTAG_SUBFILETYPE: (ctypes.c_uint32, lambda _d: _d.value),
    TIFFTAG_TILELENGTH: (ctypes.c_uint32, lambda _d: _d.value),
    TIFFTAG_TILEWIDTH: (ctypes.c_uint32, lambda _d: _d.value),
    TIFFTAG_BITSPERSAMPLE: (ctypes.c_uint16, lambda _d: _d.value),
    TIFFTAG_COMPRESSION: (ctypes.c_uint16, lambda _d: _d.value),
    TIFFTAG_ORIENTATION: (ctypes.c_uint16, lambda _d: _d.value),
    TIFFTAG_PHOTOMETRIC: (ctypes.c_uint16, lambda _d: _d.value),
    TIFFTAG_PLANARCONFIG: (ctypes.c_uint16, lambda _d: _d.value),
    TIFFTAG_JPEGQUALITY: (ctypes.c_int, lambda _d: _d.value),
    TIFFTAG_JPEGCOLORMODE: (ctypes.c_int, lambda _d: _d.value),
    TIFFTAG_YCBCRSUBSAMPLING: (ctypes.c_int, lambda _d: _d.value)
}


class TIFF(ctypes.c_void_p):
    """ Holds a pointer to TIFF object.
    To open a tiff file for reading, use
    tiff = TIFF.open (filename, more='r')
    """

    @classmethod
    def open(cls, filename, mode='r'):
        """ Open tiff file as TIFF.
        """
        tiff = LIBTIFF.TIFFOpen(filename, mode)
        if tiff.value is None:
            raise TypeError('Failed to open file ' + b'filename')
        return tiff

    def WriteDirectory(self):
        """
        WriteDirectory
        :return: None
        """
        result = LIBTIFF.TIFFWriteDirectory(self)
        assert result == 1, result

    closed = False

    def close(self, lib_tiff):
        """
        Method to close tiff file handle
        :param lib_tiff: tiff file handle
        :return: None
        """
        if not self.closed and self.value is not None:
            lib_tiff.TIFFClose(self)
            self.closed = True

    def SetField(self, tag, value, count=None):
        """
        Set TIFF field value with tag.
        tag can be numeric constant TIFFTAG_<tagname> or a
        string containing <tagname>.
        :param tag: Tiff tag
        :param value: Tag value
        :param count:
        :return: result
        """
        if isinstance(tag, str):
            tag = eval('TIFFTAG_' + tag.upper())
        tiff_tag = TIFFTAGS.get(tag)
        if tiff_tag is None:
            print('Warning: no tag %r defined' % tag)
            return None
        data_type = tiff_tag[0]
        if data_type == ctypes.c_float:
            data_type = ctypes.c_double
        result = self.libtiff_set_field_interface(count, tag, data_type, value)
        return result

    def libtiff_set_field_interface(self, count, tag, data_type, value):
        """
        libtiff_set_field_interface
        :param count:
        :param tag: TIFF TAG
        :param data_type: data type
        :param value: Tag value
        :return: result
        """
        try:
            # value is an iterable
            data = data_type(*value)
        except TypeError:
            data = data_type(value)
        if count is None:
            LIBTIFF.TIFFSetField.argtypes = LIBTIFF.TIFFSetField.argtypes[:2] + [data_type]
            result = LIBTIFF.TIFFSetField(self, tag, data)
        else:
            LIBTIFF.TIFFSetField.argtypes = LIBTIFF.TIFFSetField.argtypes[:2] + [ctypes.c_uint,
                                                                                 data_type]
            result = LIBTIFF.TIFFSetField(self, tag, count, data)
        return result


LIBTIFF.TIFFOpen.restype = TIFF
LIBTIFF.TIFFOpen.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
LIBTIFF.TIFFSetField.restype = ctypes.c_int
LIBTIFF.TIFFSetField.argtypes = [TIFF, ctypes.c_uint, ctypes.c_void_p]  # last item is reset in
# TIFF.SetField method
LIBTIFF.TIFFWriteTile.restype = ctypes.c_int32
LIBTIFF.TIFFWriteTile.argtypes = [TIFF, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32,
                                  ctypes.c_uint32, ctypes.c_uint16]
LIBTIFF.TIFFWriteEncodedTile.restype = ctypes.c_int32
LIBTIFF.TIFFWriteEncodedTile.argtypes = [TIFF, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_int32]
LIBTIFF.TIFFClose.restype = None
LIBTIFF.TIFFClose.argtypes = [TIFF]

# ################ #END-----libTIFF interfacing code------END ################
