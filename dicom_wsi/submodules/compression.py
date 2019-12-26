from io import BytesIO

import numpy as np
import pydicom
from PIL import Image


def _compress(img_arr, compression, quality):
    # JPEG Baseline (Process 1)	1.2.840.10008.1.2.4.50
    # JPEG Extended (Process 2 and 4)	1.2.840.10008.1.2.4.51
    # JPEG Lossless (Process 14)	1.2.840.10008.1.2.4.57
    # JPEG Lossless (Process 14, SV1)	1.2.840.10008.1.2.4.70
    # JPEG LS Lossless	1.2.840.10008.1.2.4.80
    # JPEG LS Lossy 3	1.2.840.10008.1.2.4.81
    # JPEG2000 Lossless	1.2.840.10008.1.2.4.90
    # JPEG2000 4	1.2.840.10008.1.2.4.91
    if compression == 'None':
        return img_arr
    elif compression == '.jpg':
        img = Image.fromarray(img_arr)
        f = BytesIO()
        img.save(f, 'JPEG', quality=int(quality))
        return f.getvalue()
    elif compression == '.j2k':
        img = Image.fromarray(img_arr)
        f = BytesIO()
        img.save(f, 'JPEG2000')
        return f.getvalue()
    else:
        from input_validation import restricted_inputs
        allowed_formats = restricted_inputs['ImageFormat']
        raise TypeError("Must provide one of: [{}]".format(allowed_formats))


def numpy_to_compressed(ndarray, dcm, compression=None, quality=75):
    """ Convert a numpy array of [N, H, W, C] to a compressed bytestring list
    :param ndarray:
    :param dcm: dicom object
    :param compression:
    :param quality: Value for compression (JPEG only)
    # https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html#jpeg
    :return: a DICOM object with PixelData

    N = Number of frames
    H = Height
    W = Width
    C = Number of channels
    """
    tile_size = ndarray.shape[1]
    num_frames = ndarray.shape[0]
    frame_offsets = range(0, num_frames, tile_size)
    tmp_image = encode_pixel_data_element_header(frame_offsets)

    for i in range(num_frames):
        img = ndarray[i, :, :, :]
        compressed_image = encode_frame_item(_compress(img, compression, quality))
        tmp_image = tmp_image + compressed_image
    tmp_image = tmp_image + encode_delimiter_item()
    dcm.PixelData = tmp_image
    dcm.LossyImageCompressionRatio = int(3)  # TODO: Do not hard-code this
    dcm.LossyImageCompression = '01'
    if compression == '.jpg':
        dcm.LossyImageCompressionMethod = 'ISO_10918_1'  # JPEG Lossy Compression
    elif compression == '.j2k':
        dcm.LossyImageCompressionMethod = 'ISO_14495_1'  # JPEG-LS Near-lossless Compression
    return dcm


def encode_frame_item(compressed_pixels, IS_LITTLE_ENDIAN=True, IS_IMPLICIT_VR=False):
    """Encodes a *Frame* item of an encapsulated *Pixel Data* element.
    Parameters
    ----------
    pixels: numpy.ndarray
        Compressed pixel data of the frame
    Returns
    -------
    bytes
        Encoded frame item
    """
    length = len(compressed_pixels)
    # Zero pad pixels to ensure length of frame item is even
    pad = False
    if (length % 2) != 0:
        length += 1
        pad = True
    with pydicom.filebase.DicomBytesIO() as fp:
        fp.is_little_endian = IS_LITTLE_ENDIAN
        fp.is_implicit_VR = IS_IMPLICIT_VR
        # Tag of Frame item
        fp.write_tag(pydicom.tag.ItemTag)
        # Length of Frame item
        fp.write_UL(length)
        # Value of Frame item
        fp.write(compressed_pixels)
        if pad:
            fp.write(np.array([0], dtype=np.uint8))
        return fp.getvalue()


def encode_pixel_data_element_header(frame_offsets, IS_LITTLE_ENDIAN=True, IS_IMPLICIT_VR=False):
    """Encodes the "header" of an encapsulated *Pixel Data* element, including
    the *Basic Offset Table* item.
    Parameters
    ----------
    frame_offsets: Sequence[int]
        Offset values of frames (position of the first byte of each *Frame*
        item from the first byte in the *Pixel Data* element following the
        *Basic Offset Table* item)
        # ?? length(encode_frame_item(pixels)) * frame number ?
    Returns
    -------
    bytes
        Encoded "header" of the pixel data element
        (including BOT but without frame items and delimiter item)
    """
    with pydicom.filebase.DicomBytesIO() as fp:
        fp.is_little_endian = IS_LITTLE_ENDIAN
        fp.is_implicit_VR = IS_IMPLICIT_VR
        data_elem_tag = pydicom.tag.TupleTag((0x7FE0, 0x0010))
        data_elem_vr = 'OB'
        data_elem_length = 0xFFFFFFFF  # undefined length
        bot_length = len(frame_offsets) * 4  # unsigned 32-bit integers
        # Tag of Pixel Data element
        fp.write_tag(data_elem_tag)
        # Value Representation of Pixel Data element
        fp.write(bytes(data_elem_vr, pydicom.charset.default_encoding))
        # Reserved
        fp.write_US(0)
        # Length of Pixel Data element
        fp.write_UL(data_elem_length)
        # Tag of Basic Offset Table item
        fp.write_tag(pydicom.tag.ItemTag)
        # Length of Basic Offset Table item
        fp.write_UL(bot_length)
        # Value of Basic Offset Table item: concatenation of integers values
        [fp.write_UL(value) for value in frame_offsets]
        return fp.getvalue()


def encode_delimiter_item(IS_LITTLE_ENDIAN=True, IS_IMPLICIT_VR=False):
    """Encodes a *Delimiter* item for an encapsulated DICOM *Pixel Data*
    element.
    Returns
    -------
    bytes
        Encoded delimiter item
    """
    with pydicom.filebase.DicomBytesIO() as fp:
        fp.is_little_endian = IS_LITTLE_ENDIAN
        fp.is_implicit_VR = IS_IMPLICIT_VR
        # Tag of Sequence Delimiter item
        fp.write_tag(pydicom.tag.SequenceDelimiterTag)
        # Length of Sequence Delimiter item
        fp.write_UL(0)
        return fp.getvalue()
