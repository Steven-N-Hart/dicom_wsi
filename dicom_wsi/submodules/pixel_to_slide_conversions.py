import logging

from pydicom.dataset import Dataset
from pydicom.sequence import Sequence

logger = logging.getLogger(__name__)


def add_PerFrameFunctionalGroupsSequence(wsi=None, ds=None, tile_size=500, series_downsample=1):
    ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows = get_wsi_size(wsi=wsi)
    tiles = generate_XY_tiles(ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows, tile_size=tile_size)
    ds.PerFrameFunctionalGroupsSequence = Sequence([])
    for i in tiles:
        x_pos, y_pos, x_tile, y_tile = i
        data_group1 = Dataset()
        dimension_index_values = Dataset()
        plane_position = Dataset()
        x, y, z = compute_slide_offsets_from_pixel_data(ds=ds, row=int(x_tile), col=int(y_tile),
                                                        series_downsample=series_downsample)
        plane_position.XOffsetInSlideCoordinateSystem = x
        plane_position.YOffsetInSlideCoordinateSystem = y
        plane_position.ZOffsetInSlideCoordinateSystem = z
        plane_position.ColumnPositionInTotalImagePixelMatrix = x_pos
        plane_position.RowPositionInTotalImagePixelMatrix = y_pos
        dimension_index_values.DimensionIndexValues = [x_tile, y_tile]
        data_group1.FrameContentSequence = Sequence([dimension_index_values])
        data_group1.PlanePositionSlideSequence = Sequence([plane_position])
        ds.PerFrameFunctionalGroupsSequence.append(data_group1)
    return ds


def generate_XY_tiles(x_max, y_max, tile_size=500):
    x_tile = 0
    y_tile = 0
    for x in range(1, int(x_max), int(tile_size)):
        x_tile += 1
        for y in range(1, int(y_max), int(tile_size)):
            y_tile += 1
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
    x = int(ds.TotalPixelMatrixOriginSequence[0][0x0040, 0x0072a].value) - (
        row * float(ds.SharedFunctionalGroupsSequence[0][0x0028, 0x9110][0][0x0028, 0x0030][1]) * series_downsample)
    y = int(ds.TotalPixelMatrixOriginSequence[0][0x0040, 0x0073a].value) - (
        col * float(ds.SharedFunctionalGroupsSequence[0][0x0028, 0x9110][0][0x0028, 0x0030][0]) * series_downsample)
    z = 0
    return x, y, z


def get_wsi_size(wsi=None):
    """
    return the size of the level 0 image slide
    :param wsi: OpenSlideObject
    :return: TotalPixelMatrixColumns, TotalPixelMatrixRows
    """
    assert wsi is not None, "You must provide a valid wsi object"
    return wsi.dimensions
