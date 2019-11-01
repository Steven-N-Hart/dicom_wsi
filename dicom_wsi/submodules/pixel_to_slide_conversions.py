import logging

import numpy as np
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence

logger = logging.getLogger(__name__)


def add_PerFrameFunctionalGroupsSequence(img=None, ds=None, tile_size=500, series_downsample=1):
    imlist = []
    x_tile = None
    y_tile = None
    max_y = 0
    max_x = 0
    np_3d = np.ndarray(buffer=img.write_to_memory(),
                       dtype=format_to_dtype[img.format],
                       shape=[img.height, img.width, 3])

    # get image size
    ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows = img.width, img.height
    tiles = generate_XY_tiles(ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows, tile_size=tile_size)
    ds.PerFrameFunctionalGroupsSequence = Sequence([])
    for i in tiles:
        x_pos, y_pos, x_tile, y_tile = i
        x_pos = int(x_pos)
        y_pos = int(y_pos)
        x_tile = int(x_tile)
        y_tile = int(y_tile)
        tile_size = int(tile_size)

        data_group1 = Dataset()
        dimension_index_values = Dataset()
        plane_position = Dataset()
        x, y, z = compute_slide_offsets_from_pixel_data(ds=ds, row=x_tile, col=y_tile,
                                                        series_downsample=series_downsample)
        plane_position.XOffsetInSlideCoordinateSystem = round(x, 5)
        plane_position.YOffsetInSlideCoordinateSystem = round(y, 5)
        plane_position.ZOffsetInSlideCoordinateSystem = round(z, 5)
        plane_position.ColumnPositionInTotalImagePixelMatrix = x_pos
        plane_position.RowPositionInTotalImagePixelMatrix = y_pos
        dimension_index_values.DimensionIndexValues = [x_tile, y_tile]
        data_group1.FrameContentSequence = Sequence([dimension_index_values])
        data_group1.PlanePositionSlideSequence = Sequence([plane_position])
        ds.PerFrameFunctionalGroupsSequence.append(data_group1)

        # Get pixel data
        x_next_step = tile_size + x_pos
        y_next_step = tile_size + y_pos
        tmp = np_3d[x_pos:x_next_step, y_pos:y_next_step, :]
        if tmp.shape == (tile_size, tile_size, 3):
            imlist.append(tmp)
        else:
            tmp3 = np.zeros((tile_size, tile_size, 3), dtype=int)
            tmp3 = np.uint8(tmp3)
            tmp = np.uint8(tmp)
            a, b, c = [int(x) for x in tmp.shape]
            tmp3[0:a, 0:b, :] = tmp
            imlist.append(tmp3)

    # stack each of the frames
    num_frames = imlist.__len__()
    ds.NumberOfFrames = num_frames
    image_array = np.zeros((num_frames, tile_size, tile_size, 3), dtype=np.int8)
    for i in range(num_frames):
        image_array[i, :, :, :] = imlist[i]
    ds.PixelData = image_array.tobytes()
    ds.Columns, ds.Rows = tile_size, tile_size
    return ds


def generate_XY_tiles(x_max, y_max, tile_size=500):
    x_tile = 0
    for x in range(1, int(x_max), int(tile_size)):
        x_tile += 1
        y_tile = 0
        for y in range(1, int(y_max), int(tile_size)):
            y_tile += 1
            logging.debug('x:{} y:{} x_tile:{} y_tile:{}'.format(x, y, x_tile, y_tile))
            yield x, y, x_tile, y_tile


def compute_slide_offsets_from_pixel_data(ds=None, row=None, col=None, series_downsample=1):
    """
    Calculate the x and y coordinate in slide space
    :param ds: some sort of DICOM object
    :param row: tile row number [Dimension Index Values (0020,9157)]
    :param col: tile column number [Dimension Index Values (0020,9157)]
    :param series_downsample: number that indicates how many divisions to apply (1 means no downsample, i.e. level 0)
    :return: x (0040,072a), y (0040,073a), and z (0040,074a) offsets
    """
    assert ds is not None, "You must provide a valid DICOM object"
    assert row is not None, "Row value should not be empty"
    assert col is not None, "Col value should not be empty"
    # BeginningPosition - RocOrColNumber * PixelSpacing * series_downsample
    # 10-25-2019 changed from - to +
    x = int(ds.TotalPixelMatrixOriginSequence[0][0x0040, 0x0072a].value) + (
        row * float(ds.SharedFunctionalGroupsSequence[0][0x0028, 0x9110][0][0x0028, 0x0030][1]) * series_downsample)
    y = int(ds.TotalPixelMatrixOriginSequence[0][0x0040, 0x0073a].value) + (
        col * float(ds.SharedFunctionalGroupsSequence[0][0x0028, 0x9110][0][0x0028, 0x0030][0]) * series_downsample)
    z = 0
    return x, y, z


# https://libvips.github.io/pyvips/intro.html#numpy-and-pil
format_to_dtype = {
    'uchar': np.uint8,
    'char': np.int8,
    'ushort': np.uint16,
    'short': np.int16,
    'uint': np.uint32,
    'int': np.int32,
    'float': np.float32,
    'double': np.float64,
    'complex': np.complex64,
    'dpcomplex': np.complex128,
}

dtype_to_format = {
    'uint8': 'uchar',
    'int8': 'char',
    'uint16': 'ushort',
    'int16': 'short',
    'uint32': 'uint',
    'int32': 'int',
    'float32': 'float',
    'float64': 'double',
    'complex64': 'complex',
    'complex128': 'dpcomplex',
}
