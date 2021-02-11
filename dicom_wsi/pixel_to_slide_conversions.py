import io
import logging

import numpy as np
from PIL import Image
from pydicom.dataset import Dataset
from pydicom.encaps import encapsulate
from pydicom.filewriter import dcmwrite
from pydicom.sequence import Sequence

from .image_filter import image_filter

logger = logging.getLogger(__name__)


def add_per_frame_functional_groups_sequence(img=None, ds=None, cfg=None, tile_size=500, series_downsample=1):
    """
    Calculate the PerFrame Functional Groups

    :param img: VIPS image object
    :param ds: DICOM Object
    :param cfg: Config dictionary
    :param tile_size: how big should each sub image be?
    :param series_downsample: Factor to translate between inches and pixels
    :return: None
    """
    imlist = []
    fragment = 0
    tile_size = int(tile_size)

    out_file_prefix = cfg.get('General').get('OutFilePrefix')
    background_range = cfg.get('General').get('background_range')
    threshold = cfg.get('General').get('threshold')
    compression_type = cfg.get('General').get('ImageFormat')
    compression_quality = int(cfg.get('General').get('CompressionAmount'))
    max_frames = int(cfg.get('General').get('MaxFrames'))
    tiled_sparse = cfg.get('BaseAttributes').get('DimensionOrganizationType')

    if tiled_sparse == 'TILED_SPARSE':
        background_range = int(cfg.get('General').get('background_range'))
        threshold = float(cfg.get('General').get('threshold'))

    np_3d = np.ndarray(buffer=img.write_to_memory(),
                       dtype=format_to_dtype[img.format],
                       shape=[img.height, img.width, img.bands])

    np_3d = np_3d[:, :, :3]  # Remove the alpha channel if there is one

    # get image size
    ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows = img.width, img.height
    ds.PerFrameFunctionalGroupsSequence = Sequence([])

    tiles = generate_xy_tiles(ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows, tile_size=tile_size)
    for i in tiles:
        x_pos, y_pos, x_tile, y_tile = i
        x_pos = int(x_pos)
        y_pos = int(y_pos)
        x_tile = int(x_tile)
        y_tile = int(y_tile)

        x, y, z = compute_slide_offsets_from_pixel_data(ds=ds, row=y_tile, col=x_tile,
                                                        series_downsample=series_downsample)

        # Get pixel data for the frame
        x_next_step = tile_size + x_pos
        y_next_step = tile_size + y_pos
        tmp = np_3d[y_pos:y_next_step, x_pos:x_next_step, :]

        # Skip images if tiled_sparse
        if tiled_sparse == 'TILED_SPARSE':
            if not image_filter(tmp, background_range=background_range, threshold=threshold):
                # Skip to avoid background tiles
                logger.debug('Skipping {} {}'.format(x_pos, y_pos))
                continue

        # Make sure the frame is square and filled
        imlist.append(ensure_even_image(tmp, tile_size))

        data_group1 = define_plane_position_slide_sequence(x, y, z, x_tile, y_tile, x_pos, y_pos)
        ds.PerFrameFunctionalGroupsSequence.append(data_group1)

        # If the number of frames matches the limit, then save so the file doesn't get too big
        if imlist.__len__() == max_frames:
            fragment += 1
            ds = add_imgdata(imlist, ds, tile_size, compression_type, compression_quality)
            out_file = out_file_prefix + '.' + str(ds.InstanceNumber) + '-' + str(fragment) + '.dcm'

            dcmwrite(out_file, ds, write_like_original=False)
            logger.info('Compressed {} image frames into {}'.format(imlist.__len__(), out_file))
            # Empty out contents so they don't get duplicated frames in each file
            imlist = []
            ds.PerFrameFunctionalGroupsSequence = None

    ds = add_imgdata(imlist, ds, tile_size, compression_type, compression_quality)
    out_file = out_file_prefix + '.' + str(ds.InstanceNumber) + '-' + str(fragment) + '.dcm'

    dcmwrite(out_file, ds, write_like_original=False)
    logger.info('Compressed {} image frames into {}'.format(imlist.__len__(), out_file))
    return 1


def add_imgdata(imlist, ds, tile_size, compression_type, compression_quality):
    """
    Calls the compression algorithm and add to DICOM object

    :param imlist: list of images to compress
    :param ds: DICOM object
    :param tile_size: how large the image tiles should be
    :param compression_type: name of compression scheme
    :param compression_quality: quality of compression
    :return: DICOM object with pixel data
    """
    num_frames = imlist.__len__()
    ds.NumberOfFrames = int(num_frames)
    image_array = np.zeros((num_frames, tile_size, tile_size, 3), dtype=np.uint8)

    # stack each of the frames
    for q in range(num_frames):
        image_array[q, :, :, :] = imlist[q]

    if compression_type == 'None':
        ds.PixelData = image_array.tobytes()
        ds.LossyImageCompression = '00'
    else:
        ds = compress_img_list(ds, imlist, num_frames, compression_type, compression_quality)

    ds.Columns, ds.Rows = tile_size, tile_size  # used to calculate expected size in validator
    return ds


def define_plane_position_slide_sequence(x, y, z, x_tile, y_tile, x_pos, y_pos):
    """
    Build up the sequence position structure for the coordinates

    :param x: offset position on slide
    :param y: offset position on slide
    :param z: offset position on slide (usually 1)
    :param x_tile: tile position number
    :param y_tile: tile position number
    :param x_pos: pixel position
    :param y_pos: pixel position
    :return: a dataset value to be appended to the PerFrameFunctionalGroupsSequence
    """
    data_group1 = Dataset()
    dimension_index_values = Dataset()
    plane_position = Dataset()

    plane_position.XOffsetInSlideCoordinateSystem = round(x, 5)
    plane_position.YOffsetInSlideCoordinateSystem = round(y, 5)
    plane_position.ZOffsetInSlideCoordinateSystem = round(z, 5)
    plane_position.ColumnPositionInTotalImagePixelMatrix = x_pos
    plane_position.RowPositionInTotalImagePixelMatrix = y_pos
    dimension_index_values.DimensionIndexValues = [x_tile, y_tile]
    data_group1.FrameContentSequence = Sequence([dimension_index_values])
    data_group1.PlanePositionSlideSequence = Sequence([plane_position])
    return data_group1


def generate_xy_tiles(x_max, y_max, tile_size=500):
    """
    Iterate through the slide with a step size of `tile_size`

    :param x_max:
    :param y_max:
    :param tile_size:
    :return: ( tile position on the x plane,
                tile position on the y plane,
                index of the tile on the x plane,
                index of the tile on the y plane)

    """
    x_tile = 0
    tile_size = int(tile_size)
    for x in range(1, int(x_max), tile_size):
        x_tile += 1
        y_tile = 0
        for y in range(1, int(y_max), tile_size):
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
    x = int(ds.TotalPixelMatrixOriginSequence[0][0x0040, 0x0072a].value) - (
        row * float(ds.SharedFunctionalGroupsSequence[0][0x0028, 0x9110][0][0x0028, 0x0030][1]) * series_downsample)
    y = int(ds.TotalPixelMatrixOriginSequence[0][0x0040, 0x0073a].value) - (
        col * float(ds.SharedFunctionalGroupsSequence[0][0x0028, 0x9110][0][0x0028, 0x0030][0]) * series_downsample)
    z = 0
    return x, y, z


def ensure_even_image(tmp, tile_size):
    """
    Images must be an even before being compressed

    :param tmp: numpy array of image values
    :param tile_size: desired output size
    :return: an even numbered shape for the numpy array
    """
    if tmp.shape == (tile_size, tile_size, 3):
        tmp_img = Image.fromarray(tmp)
    else:
        tmp3 = np.zeros((tile_size, tile_size, 3), dtype=int)
        tmp3 = np.uint8(tmp3)
        tmp = np.uint8(tmp)
        a, b, c = [int(x) for x in tmp.shape]
        tmp3[0:a, 0:b, 0:c] = tmp
        tmp_img = Image.fromarray(tmp3)
    return tmp_img


# TODO: Make this faster!!!
def compress_img_list(ds, imlist, num_frames, compression_type, compression_quality):
    f = io.BytesIO()
    imlist[0].save(f, format='tiff', append_images=imlist[1:], save_all=True, compression='None')
    # The BytesIO object cursor is at the end of the object, so I need to tell it to go back to the front
    f.seek(0)
    img = Image.open(f)
    img_byte_list = []
    # Get each one of the frames converted to even numbered bytes

    if compression_type == '.jpg':
        compression_type = 'JPEG'
        compression_method = 'ISO_10918_1'
    elif compression_type == '.jp2':
        compression_type = 'JPEG2000'
        compression_method = 'ISO_15444_1'

    for i in range(num_frames):
        try:
            img.seek(i)
            with io.BytesIO() as output:
                img.save(output, format=compression_type, quality=compression_quality)
                img_byte_list.append(output.getvalue())
        except EOFError:
            # Not enough frames in img
            break

    ds.PixelData = encapsulate(img_byte_list)
    ds['PixelData'].is_undefined_length = True
    ds.is_implicit_VR = False
    ds.LossyImageCompression = '01'
    ds.LossyImageCompressionRatio = 100 - compression_quality
    ds.LossyImageCompressionMethod = compression_method
    return ds


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
