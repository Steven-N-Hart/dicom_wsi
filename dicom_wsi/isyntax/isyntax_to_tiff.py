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
This sample code generates regular/big tiff for a desired ROI.
The common inputs to the file are:
  1. Path of the iSyntax file
  2. Regular/Big Tiff (if 0 is passed regular tiff is generated,
      whereas if 1 is passed big tiff is generated)
  3. NotSparse/Sparse (if 0 is passed sparse tiff is not generated,
      whereas if 1 is passed sparse tiff is generated)
  4. Start_level (The tiff file is generated from starting level.)
Eg:
Command for regular tiff from level 0:
  python isyntax_to_tiff.py <Isyntax file path> 0 0 0
Command for big tiff from level 0:
  python isyntax_to_tiff.py <Isyntax file path> 1 0 0
Command for regular sparse tiff from level 0:
  python isyntax_to_tiff.py <Isyntax file path> 0 1 0
Command for big sparse tiff from level 0:
  python isyntax_to_tiff.py <Isyntax file path> 1 1 0
IMPORTANT NOTE : This sample code uses libtiff.
 One needs to download it for the target platform.

On Windows:
 Download a suitable version of libtiff or build it from GitHub source.
 Required DLL's:
    libtiff-5.dll, libjpeg-62.dll, zlib1.dll

On Ubuntu: To install libtiff, execute 'apt-get install -y libtiff5-dev'

Dependencies:
    Pip modules: numpy
"""

import argparse
import os
import traceback

import numpy as np
import pixelengine
import softwarerenderbackend
import softwarerendercontext
from libtiff_interface import *


def write_tiff_tile(tiff_handle, offset, level, sparse, data, data_size, bb_list, region):
    """
    Save extracted regions as Patches to Disk
    :param tiff_handle: Tiff file handle
    :param offset: List of Offset Indices
    :param level: Level of Tile
    :param sparse: Sparse Flag
    :param data: Buffer
    :param data_size: Size of buffer
    :param bb_list: Bounding box list
    :param region : Current region
    :return: None
    """
    try:
        # check sparse and background tiles
        if sparse == 1:
            is_background = is_background_tile(bb_list, region.range)
            if is_background:
                print("Background Tile")
                print(region.range)
                return
        # Write Tile
        if LIBTIFF.TIFFWriteEncodedTile(tiff_handle, LIBTIFF.TIFFComputeTile
            (tiff_handle, offset[0], offset[1],
             level, 0), data, data_size) < 0:
            print("Error in generating TIFF")

    except RuntimeError:
        traceback.print_exc()


def is_background_tile(bb_list, bb_range):
    """
    Method to check background tile
    :param bb_list: Data envelope list
    :param bb_range: Tile view range
    :return: outside_x or outside_y
    """
    outside_x = True
    outside_y = True
    for data_envelope in bb_list:
        if (not ((bb_range[0] < data_envelope[0] and bb_range[1] < data_envelope[0]) or
                 (bb_range[0] > data_envelope[1] and bb_range[1] > data_envelope[1]))):
            outside_x = False
            break
    for data_envelope in bb_list:
        if (not ((bb_range[2] < data_envelope[2] and bb_range[3] < data_envelope[2]) or
                 (bb_range[2] > data_envelope[3] and bb_range[3] > data_envelope[3]))):
            outside_y = False
            break
    return outside_x or outside_y


def tiff_tile_processor(pixel_engine, tile_width, tile_height, level, patches,
                        patch_identifier, tiff_file_handle, bb_list, sparse):
    """
    Tiff Tile Processor
    :param pixel_engine: Object of pixel Engine
    :param tile_width: Tile Width
    :param tile_height: Tile Height
    :param level: Level
    :param patches: List of patches
    :param patch_identifier: Identifier list to map patches when fetched from pixel engine
    :param tiff_file_handle: Tiff file handle
    :param bb_list: Bounding Box List
    :param sparse: Sparse Flag
    :return: None
    """
    view = pixel_engine["in"].SourceView()
    samples_per_pixel = 3  # As we queried RGB for Pixel Data
    patch_data_size = int((tile_width * tile_height * samples_per_pixel))
    data_envelopes = view.dataEnvelopes(level)
    print("Requesting patches. Preparing patch definitions...")
    regions = view.requestRegions(patches, data_envelopes, True, [255, 0, 0],
                                  pixel_engine.BufferType(0))
    print("Request Complete. Patch definitions ready.")
    while regions:
        print("Requesting regions batch")
        regions_ready = pixel_engine.waitAny(regions)
        print("Regions returned = " + str(len(regions_ready)))
        for region in regions_ready:
            # Find the index of obtained Region in Original PatchList
            patch_id = patch_identifier[regions.index(region)]
            x_spatial = patch_id[0]
            y_spatial = patch_id[1]
            patch = np.empty(int(patch_data_size)).astype(np.uint8)
            region.get(patch)
            # Set the spatial location to paste in the TIFF file
            x_value = x_spatial * tile_width
            y_value = y_spatial * tile_height
            write_tiff_tile(tiff_file_handle, [x_value, y_value], level, sparse,
                            patch.ctypes.data, patch_data_size, bb_list, region)
            regions.remove(region)
            patch_identifier.remove(patch_id)


def find_bounding_boxes(view, level):
    """
    Method to create bounding box list
    :param view: Source View
    :param level: Current Level
    :return: bb_list
    """
    bb_list = []
    data_envelope = []
    step = 0
    for envelope in view.dataEnvelopes(level).dataEnvelopes():
        evalute = lambda envelope: (len(envelope) == 0 or
                                    len(envelope[1]) == 0 or len(envelope) > 2)
        if evalute(envelope):
            print("Data envelope is not having indices")
        else:
            print("Data envelope_" + str(step) + ": " + str(envelope[1]))
            data_envelope.append(envelope[1])
            data_env = data_envelope[step]
            final_range = create_view_range(data_env, level)
            bb_list.append(final_range)
            step = step + 1
    return bb_list


def create_view_range(data_env, level):
    """
    Create view range for every data envelope
    :param data_env: Data Envelope Indices
    :param level: level of isyntax file
    :return: View range of Data Envelope
    """
    x_final_list = []
    y_final_list = []
    for index in range(0, len(data_env)):
        x_final_list.append(data_env[index][0])
        y_final_list.append(data_env[index][1])
    # Creating a list of the input argument
    x_start = min(x_final_list)
    y_start = min(y_final_list)
    x_end = max(x_final_list)
    y_end = max(y_final_list)
    final_range = [x_start, (x_end - (2 ** level)), y_start, (y_end - (2 ** level)),
                   level]
    return final_range


def calculate_tiff_dimensions(view, start_level):
    """
    Set the TIFF tile size
    Note that TIFF mandates tile size in multiples of 16
    Calculate the Image Dimension range from the View at the Start Level
    :param view: Source View
    :param start_level: Starting Level
    :return: tiff_dim_x, tiff_dim_y
    """
    x_start = view.dimensionRanges(start_level)[0][0]
    x_end = view.dimensionRanges(start_level)[0][2]
    y_start = view.dimensionRanges(start_level)[1][0]
    y_end = view.dimensionRanges(start_level)[1][2]
    range_x = x_end - x_start
    range_y = y_end - y_start

    # As the multi-resolution image pyramid in TIFF
    #  shall follow a down sample factor of 2
    # Normalize the Image Dimension from the coarsest level
    #  so that a downscale factor of 2 is maintained across levels
    # Size Normalization
    tiff_dim_x = int(range_x / TIFF_TILE_WIDTH) * TIFF_TILE_WIDTH
    tiff_dim_y = int(range_y / TIFF_TILE_HEIGHT) * TIFF_TILE_HEIGHT

    print("Pad the image boundaries, if the width or height is not an integer multiple of the "
          "tile size")
    mod_x = range_x % TIFF_TILE_WIDTH
    mod_y = range_y % TIFF_TILE_HEIGHT
    print(mod_x, mod_y)
    if mod_x > 0:
        tiff_dim_x += TIFF_TILE_WIDTH
    if mod_y > 0:
        tiff_dim_y += TIFF_TILE_HEIGHT
    return tiff_dim_x, tiff_dim_y


def check_mod(mod, num_patches):
    """
    Checking mod value
    :param mod: modulus value
    :param num_patches: Number of patches
    :return: num_patches
    """
    if mod > 0:
        num_patches += 1
    return num_patches


def create_tiff_from_isyntax(pixel_engine, tiff_file_handle, start_level,
                             num_levels, sparse):
    """
    Method to create tiff from isyntax file
    :param pixel_engine: Object of Pixel Engine
    :param tiff_file_handle: Tiff file handle
    :param start_level: Start level
    :param num_levels: max levels in isyntax file
    :param sparse: Sparse Flag
    :return: 0
    """
    view = pixel_engine["in"].SourceView()
    tiff_dim_x, tiff_dim_y = calculate_tiff_dimensions(view, start_level)

    #  Scanned Tissue Area
    # Level 0 represents 40x scan factor
    # So, in order save time and as per the requirement,
    #  one can start from a coarser resolution level say level 2 (10x)

    sub_level = False
    for level in range(start_level, num_levels + 1, 1):
        # Take starting point as the dimensionRange start on the View
        #  for a particular Level
        x_start = view.dimensionRanges(level)[0][0]
        x_end = x_start + tiff_dim_x
        y_start = view.dimensionRanges(level)[1][0]
        y_end = y_start + tiff_dim_y

        # As the index representation is always in Base Level i.e. Level0, but
        # the step size increase with level as (2**level)
        width_patch_level = TIFF_TILE_WIDTH * (2 ** level)
        height_patch_level = TIFF_TILE_HEIGHT * (2 ** level)
        width_roi = x_end - x_start
        height_roi = y_end - y_start

        print("TIFF ROI Start and End Indices at Level - " + str(level))
        print("xStart, xEnd, yStart, yEnd, width, height")
        print(x_start, x_end, y_start, y_end, width_roi, height_roi)

        num_patches_x = int(width_roi / width_patch_level)
        num_patches_y = int(height_roi / height_patch_level)
        print("Pad the image boundaries if the width or height is not an integer multiple of the "
              "patch size")
        mod_x = width_roi % width_patch_level
        mod_y = height_roi % height_patch_level
        print(mod_x, mod_y)
        num_patches_x = check_mod(mod_x, num_patches_x)
        num_patches_y = check_mod(mod_y, num_patches_y)

        print("Number of Tiles in X and Y directions " + str(num_patches_x) + "," + str(
            num_patches_y))
        # Error Resilience: Just in case if the number of patches at a given level in either
        # direction is 0, no point in writing tiff directory
        if num_patches_x * num_patches_y <= 0:
            print("TIFF Directory Write bypassed")
            continue

        level_scale_factor = 2 ** level
        # For subdirectories corresponding to the multi-resolution pyramid, set the following
        # Tag for all levels but the initial level
        if sub_level:
            set_attribute(tiff_file_handle, TIFFTAG_SUBFILETYPE, FILETYPE_REDUCEDIMAGE)

        sub_level = True
        use_rgb = False  # Flag to choose bewteen RGB and YCbCr color model
        # Setting TIFF file attributes
        set_attribute(tiff_file_handle, TIFFTAG_IMAGEWIDTH, int(tiff_dim_x / level_scale_factor))
        set_attribute(tiff_file_handle, TIFFTAG_IMAGELENGTH, int(tiff_dim_y / level_scale_factor))
        set_attribute(tiff_file_handle, TIFFTAG_TILEWIDTH, TIFF_TILE_WIDTH)
        set_attribute(tiff_file_handle, TIFFTAG_TILELENGTH, TIFF_TILE_HEIGHT)
        set_tiff_file_attributes(tiff_file_handle, use_rgb)
        patches, patch_identifier = create_patch_list(num_patches_x, num_patches_y,
                                                      [x_start, y_start], level,
                                                      [width_patch_level, height_patch_level])
        bb_list = []
        if sparse == 1:
            bb_list = find_bounding_boxes(view, level)
        # Extract and Write TIFF Tiles
        tiff_tile_processor(pixel_engine, TIFF_TILE_WIDTH, TIFF_TILE_HEIGHT, level,
                            patches, patch_identifier,
                            tiff_file_handle, bb_list, sparse)
        tiff_file_handle.WriteDirectory()
    return 0


def set_attribute(tiff_file_handle, key, value):
    """
    Set Tiff file attributes
    :param tiff_file_handle: Tiff file handle
    :param key: Associated key
    :param value: value of key
    :return: None
    """
    assert tiff_file_handle.SetField(key, value) == 1, \
        "could not set " + str(key) + " tag"


def set_tiff_file_attributes(tiff_file_handle, use_rgb):
    """
    Setting tiff file common attributes
    :param tiff_file_handle: Tiff file handle
    :param use_rgb: RGB Flag
    :return: None
    """
    set_attribute(tiff_file_handle, TIFFTAG_BITSPERSAMPLE, BITSPERSAMPLE)
    set_attribute(tiff_file_handle, TIFFTAG_SAMPLESPERPIXEL, SAMPLESPERPIXEL)
    set_attribute(tiff_file_handle, TIFFTAG_PLANARCONFIG, PLANARCONFIG)
    set_attribute(tiff_file_handle, TIFFTAG_COMPRESSION, COMPRESSION_JPEG)
    set_attribute(tiff_file_handle, TIFFTAG_JPEGQUALITY, JPEGQUALITY)
    set_attribute(tiff_file_handle, TIFFTAG_ORIENTATION, ORIENTATION_TOPLEFT)

    if use_rgb:
        set_attribute(tiff_file_handle, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_RGB)
    else:
        set_attribute(tiff_file_handle, TIFFTAG_PHOTOMETRIC, PHOTOMETRIC_YCBCR)
        set_attribute(tiff_file_handle, TIFFTAG_JPEGCOLORMODE, JPEGCOLORMODE_RGB)
        assert tiff_file_handle.SetField(TIFFTAG_YCBCRSUBSAMPLING, YCBCRHORIZONTAL,
                                         YCBCRVERTICAL) == 1, "could not set YCbCr subsample tag"


def create_patch_list(num_patches_x, num_patches_y, starting_indices, level, patch_size):
    """
    Method to create patches list and patch identifier list
    :param num_patches_x: Number of patches in x
    :param num_patches_y: Number of patches in y
    :param starting_indices: Starting indices
    :param level: Level
    :param patch_size: Size of patch
    :return: list of patches, patch_identifier
    """
    patches = []
    patch_identifier = []
    y_spatial = 0
    for y_counter in range(num_patches_y):
        y_patch_start = starting_indices[1] + (y_counter * patch_size[1])
        y_patch_end = y_patch_start + patch_size[1]
        x_spatial = 0
        for x_counter in range(num_patches_x):
            x_patch_start = starting_indices[0] + (x_counter * patch_size[0])
            x_patch_end = x_patch_start + patch_size[0]
            patch = [x_patch_start, x_patch_end - 2 ** level, y_patch_start,
                     y_patch_end - 2 ** level, level]
            patches.append(patch)
            patch_identifier.append([x_spatial, y_spatial])
            x_spatial += 1
        y_spatial += 1
    return patches, patch_identifier


def encode_file_path(file_path):
    """
    Method to encode file_path as per python version
    :param file_path: file_path
    :return: file_path
    """
    if sys.version_info[0] < 3:
        file_path = unicode(file_path, "utf-8")
    else:
        file_path = bytes(file_path, encoding='utf-8')
    return file_path


def get_tiff_handle(tiff_type, input_file, sparse):
    """
    Method to generate tiff file handle
    :param tiff_type: Type of tiff
    :param input_file: Input file
    :param sparse: Sparse flag
    :return: tiff_file_handle
    """
    file_name = ".tiff"
    if sparse:
        file_name = "_sparse" + file_name
    image_name = os.path.splitext(os.path.basename(input_file))[0]

    if tiff_type == 0:
        print("Regular Tiff")
        file_path = "." + os.path.sep + image_name + file_name
        file_path = encode_file_path(file_path)

        tiff_file_handle = TIFF.open(file_path, mode=b'w')
    elif tiff_type == 1:
        print("Big Tiff")
        file_path = "." + os.path.sep + image_name + "_BIG" + file_name
        file_path = encode_file_path(file_path)
        tiff_file_handle = TIFF.open(file_path, mode=b'w8')

    return tiff_file_handle


def main():
    """
    Main Method
    :return: None
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input",
                        dest='input',
                        help="Image File")

    parser.add_argument("-t", "--tif",
                        dest="tif",
                        choices=['TIFF', 'BIGTIFF'],
                        default="BIGTIFF",
                        help="TIFF/BIGTIFF")

    parser.add_argument("-s", "--sparse",
                        dest='sparse',
                        type=bool,
                        default=False,
                        help="If the image should be sparse or not")
    parser.add_argument("-l", "--startlevel",
                        dest='startlevel',
                        type=int,
                        default=0,
                        help="Level at which to do the conversion")

    args = parser.parse_args()

    # Initializing the pixel engine
    render_context = softwarerendercontext.SoftwareRenderContext()
    render_backend = softwarerenderbackend.SoftwareRenderBackend()
    pixel_engine = pixelengine.PixelEngine(render_backend, render_context)
    pixel_engine["in"].open(args.input)
    start_level = int(args.startlevel)
    if args.tif == 'BIGTIFF':
        tiff_type = 1
    else:
        tiff_type = 0
    sparse = int(args.sparse)
    if not (0 <= sparse <= 1 and 0 <= tiff_type <= 1):
        print("Invalid arguments passed")
        return
    tiff_file_handle = get_tiff_handle(tiff_type, args.input, sparse)

    num_levels = pixel_engine["in"].numLevels()
    if 0 <= start_level < num_levels:
        print("Generating TIFF, Please Wait.....")
        result = create_tiff_from_isyntax(pixel_engine, tiff_file_handle, start_level,
                                          int(num_levels),
                                          sparse)
        # Close the TIFF file handle.
        LIBTIFF.TIFFClose(tiff_file_handle)
        if result == 0:
            print("TIFF Successfully Generated")
        else:
            print("Error in generating TIFF")
    else:
        print("Invalid start_level Input")
    pixel_engine["in"].close()


if __name__ == '__main__':
    main()
