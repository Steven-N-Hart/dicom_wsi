import io
import pydicom
import logging
from io import BytesIO
import numpy as np
from PIL import Image
from pydicom.dataset import Dataset, FileDataset, DataElement
from pydicom.encaps import encapsulate
from pydicom.filewriter import dcmwrite
from pydicom.sequence import Sequence

logger = logging.getLogger(__name__)


def create_pixel_data(img_list, compression_type, q):
    if compression_type == 'None':
        instance_byte_str = b''
        for img in img_list:
            instance_byte_str += img.tobytes()
        return instance_byte_str
    else:
        encoded_framed_items = []
        for img in img_list:
            instance_byte_str_buffer = BytesIO()
            img.save(instance_byte_str_buffer, "JPEG", quality=q, icc_profile=img.info.get('icc_profile'),
                     progressive=False)
            t = instance_byte_str_buffer.getvalue()
            encoded_framed_items.append(t)
        return encoded_framed_items

def add_PerFrameFunctionalGroupsSequence(img=None, ds=None, cfg=None, tile_size=500, series_downsample=1):
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
    x_tile = None
    y_tile = None
    fragment = 1
    tile_size = int(tile_size)
    out_file_prefix = cfg.get('General').get('OutFilePrefix')
    np_3d = np.ndarray(buffer=img.write_to_memory(),
                       dtype=format_to_dtype[img.format],
                       shape=[img.height, img.width, img.bands])

    np_3d = np_3d[:, :, :3]  # Remove the alpha channel if there is one

    # get image size
    ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows = img.width, img.height
    ds.PerFrameFunctionalGroupsSequence = Sequence([])

    compression_type = cfg.get('General').get('ImageFormat')
    compression_quality = cfg.get('General').get('CompressionAmount')
    # logger.debug('compression_type: {}'.format(compression_type))

    # If the number of frames matches the limit, then save so the file doesn't get too big
    max_frames = int(cfg.get('General').get('MaxFrames'))

    tiles = generate_XY_tiles(ds.TotalPixelMatrixColumns, ds.TotalPixelMatrixRows, tile_size=tile_size)
    for i in tiles:
        x_pos, y_pos, x_tile, y_tile = i
        x_pos = int(x_pos)
        y_pos = int(y_pos)
        x_tile = int(x_tile)
        y_tile = int(y_tile)

        data_group1 = Dataset()
        dimension_index_values = Dataset()
        plane_position = Dataset()
        x, y, z = compute_slide_offsets_from_pixel_data(ds=ds, row=y_tile, col=x_tile,
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

        # Get pixel data for the frame
        x_next_step = tile_size + x_pos
        y_next_step = tile_size + y_pos
        tmp = np_3d[y_pos:y_next_step, x_pos:x_next_step, :]

        # Make sure the frame is square and filled
        if tmp.shape == (tile_size, tile_size, 3):
            tmp_img = Image.fromarray(tmp)
            imlist.append(tmp_img)
        else:
            tmp3 = np.zeros((tile_size, tile_size, 3), dtype=int)
            tmp3 = np.uint8(tmp3)
            tmp = np.uint8(tmp)
            a, b, c = [int(x) for x in tmp.shape]
            tmp3[0:a, 0:b, 0:c] = tmp
            tmp_img = Image.fromarray(tmp3)
            imlist.append(tmp_img)

        if imlist.__len__() == max_frames:
            logger.debug('imlist.__len__() {} == max_frames {}'.format(imlist.__len__(), max_frames))
            ds.NumberOfFrames = max_frames

            encoded_pixel_data = create_pixel_data(imlist, compression_type, compression_quality)

            if compression_type == 'None':
                data_elem_tag = pydicom.tag.TupleTag((0x7FE0, 0x0010))
                enc_frames = encapsulate(encoded_pixel_data, has_bot=True)
                pd_ele = DataElement(data_elem_tag, 'OB', enc_frames, is_undefined_length=True)
                ds.add(pd_ele)

            else:
                ds.PixelData = encoded_pixel_data

            ds.Columns, ds.Rows = tile_size, tile_size  # used to calculate expected size
            out_file = out_file_prefix + '.' + str(ds.InstanceNumber) + '-' + str(fragment) + '.dcm'

            dcmwrite(out_file, ds, write_like_original=False)
            logger.info('Wrote: {}'.format(out_file))

    #
    #         self.dcm_instance.file_meta = file_meta
    #         self.dcm_instance.save_as(filename, write_like_original=False)
    #         self.instance_cnt += 1
    #
    #
    #         image_array = np.zeros((num_frames, tile_size, tile_size, 3), dtype=np.int8)
    #         for q in range(num_frames):
    #             image_array[q, :, :, :] = imlist[q]
    #         #logger.debug('image_array is {}'.format(image_array))
    #         if compression_type == 'None':
    #             ds.PixelData = image_array.tobytes()
    #             ds.LossyImageCompression = '00'
    #         else:
    #             f = io.BytesIO()
    #             imlist[0].save(f, format='tiff', append_images=imlist[1:], save_all=True, compression='jpeg')
    #             # The BytesIO object cursor is at the end of the object, so I need to tell it to go back to the front
    #             f.seek(0)
    #             img = Image.open(f)
    #             img_byte_list = []
    #             # Get each one of the frames converted to even numbered bytes
    #             for i in range(num_frames):
    #                 try:
    #                     img.seek(i)
    #                     with io.BytesIO() as output:
    #                         img.save(output, format='jpeg')
    #                         img_byte_list.append(output.getvalue())
    #                 except EOFError:
    #                     # Not enough frames in img
    #                     break
    #
    #             ds.PixelData = encapsulate(img_byte_list)
    #             ds['PixelData'].is_undefined_length = True
    #             ds.is_implicit_VR = False
    #             ds.LossyImageCompression = '01'
    #             ds.LossyImageCompressionRatio = 10
    #             ds.LossyImageCompressionMethod = 'ISO_10918_1'
    #
    #         ds.Columns, ds.Rows = tile_size, tile_size
    #         fragment += 1
    #         # ds.save_as(out_file)
    #         dcmwrite(out_file, ds, write_like_original=False)
    #         logger.info('Wrote: {}'.format(out_file))
    #         # Empty out contents so they don't get duplicated frames in each file
    #         imlist = []
    #         ds.PerFrameFunctionalGroupsSequence = None
    #
    # # stack each of the frames
    # num_frames = imlist.__len__()
    # ds.NumberOfFrames = int(num_frames)
    # image_array = np.zeros((num_frames, tile_size, tile_size, 3), dtype=np.uint8)
    #
    # for q in range(num_frames):
    #     image_array[q, :, :, :] = imlist[q]
    #
    # if compression_type == 'None':
    #     ds.PixelData = image_array.tobytes()
    #     ds.LossyImageCompression = '00'
    # else:
    #     # ds = numpy_to_compressed(image_array, ds, compression=compression_type, quality=compression_quality)
    #     f = io.BytesIO()
    #     imlist[0].save(f, format='tiff', append_images=imlist[1:], save_all=True, compression='jpeg')
    #     # The BytesIO object cursor is at the end of the object, so I need to tell it to go back to the front
    #     f.seek(0)
    #     img = Image.open(f)
    #     img_byte_list = []
    #     # Get each one of the frames converted to even numbered bytes
    #     for i in range(num_frames):
    #         try:
    #             img.seek(i)
    #             with io.BytesIO() as output:
    #                 img.save(output, format='jpeg')
    #                 img_byte_list.append(output.getvalue())
    #         except EOFError:
    #             # Not enough frames in img
    #             break
    #
    #     ds.PixelData = encapsulate(img_byte_list)
    #     ds['PixelData'].is_undefined_length = True
    #     ds.is_implicit_VR = False
    #     ds.LossyImageCompression = '01'
    #     ds.LossyImageCompressionRatio = 10
    #     ds.LossyImageCompressionMethod = 'ISO_10918_1'
    #
    # ds.Columns, ds.Rows = tile_size, tile_size  # used to calculate expected size
    # out_file = out_file_prefix + '.' + str(ds.InstanceNumber) + '-' + str(fragment) + '.dcm'
    #
    # dcmwrite(out_file, ds, write_like_original=False)
    # logger.info('Wrote: {}'.format(out_file))



def generate_XY_tiles(x_max, y_max, tile_size=500):
    """
    Iterate through the slide with a step size of `tile_size`
    :param x_max:
    :param y_max:
    :param tile_size:
    :return:
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

