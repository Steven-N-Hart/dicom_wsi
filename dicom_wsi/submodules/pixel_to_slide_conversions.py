def add_PerFrameFunctionalGroupsSequence(wsi=None, ds=None, tile_size=500, SeriesDownsample=1):
    ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows = get_wsi_size(wsi=wsi)
    tiles = generate_XY_tiles(ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows, tile_size=tile_size)
    for i in tiles:
        x, y, z = compute_slide_offsets_from_pixel_data(ds=None, Row=None, Col=None, SeriesDownsample=1)
        ########################################################################
        # NOT COMPLETE
        ########################################################################
        # ds.PerFrameFunctionalGroupsSequence.append()


def generate_XY_tiles(x_max, y_max, tile_size=500):
    x_tile = 0
    y_tile = 0
    for x in range(1, x_max, tile_size):
        x_tile += 1
        for y in range(1, y_max, tile_size):
            y_tile += 1
            yield x, y, x_tile, y_tile


def compute_slide_offsets_from_pixel_data(ds=None, Row=None, Col=None, SeriesDownsample=1):
    """
    Calculate the x and y coordinate in slide space
    :param ds: some sort of DICOM object
    :param Row: tile row number [Dimension Index Values (0020,9157)]
    :param Col: tile column number [Dimension Index Values (0020,9157)]
    :param SeriesDownsample: number that indicates how many divisions to apply (1 means no downsample, i.e. level 0)
    :return: x (0040,072a), y (0040,073a), and z (0040,074a) offsets
    """
    assert ds is not None, "You must provide a valid DICOM object"
    assert Row is not None, "Row value should not be empty"
    assert Col is not None
    "Col value should not be empty"

    # BeginningPosition - RocOrColNumber * PixelSpacing * SeriesDownsample
    x = int(ds.TotalPixelMatrixOriginSequence[0][0x0040, 0x0072a].value) - \
        (Row * float(ds.SharedFunctionalGroupsSequence[0][0x0028, 0x9110][0][0x0028, 0x0030][1]) * SeriesDownsample)
    y = int(ds.TotalPixelMatrixOriginSequence[0][0x0040, 0x0073a].value) - \
        (Col * float(ds.SharedFunctionalGroupsSequence[0][0x0028, 0x9110][0][0x0028, 0x0030][0]) * SeriesDownsample)
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
