import datetime
import logging
import tempfile

import pydicom
from pydicom.dataset import Dataset, FileDataset
# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences
from submodules.utils import add_data


# noinspection PyUnresolvedReferences
def build_base(cfg, dcm=None, dict_element='BaseAttributes', instance=1):
    base_dict = cfg[dict_element]
    logging.debug('Beginning {} Module'.format(dict_element))

    # Define hard coded variables
    # VL Whole Slide Microscopy Image Storage
    # http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_B.5.html
    compression_type = cfg.get('General').get('ImageFormat')

    media_storage_sop_instance_uid = '1.2.276.0.7230010.3.1.4.8323329.20175.1573232572.237464'
    media_storage_sop_class_uid = '1.2.840.10008.5.1.4.1.1.77.1.6'  # VL Whole Slide Microscopy Image Storage
    implementation_class_uid = '1.2.276.0.7230010.3.0.3.6.2'
    sop_instance_uid = pydicom.uid.generate_uid(prefix=None)
    file_meta_information_version = b'\x00\x01'
    implementation_version_name = 'OFFIS_DCMTK_362'
    file_meta_information_group_length = 206  # TODO: Not sure what this should be exactly

    if dict_element == 'BaseAttributes':
        suffix = '.' + str(instance) + '.dcm'
        filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name

        file_meta = Dataset()

        if compression_type == 'None':
            # noinspection PyPep8,PyUnresolvedReferences
            file_meta.TransferSyntaxUID = pydicom.uid.UncompressedPixelTransferSyntaxes[
                1]  # Implicit VR Endian: Default Transfer Syntax for DICOM
        elif compression_type == '.jpg':
            # noinspection PyUnresolvedReferences
            file_meta.TransferSyntaxUID = pydicom.uid.JPEGBaseline  # JPEG Baseline(Process 1)
        elif compression_type == '.j2k':
            file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.4.80'  # JPEG-LS Lossless Image Compression
        else:
            raise ValueError('Compression type {} is not yet supported'.format(compression_type))
        logging.debug('TransferSyntaxUID {} '.format(file_meta.TransferSyntaxUID))

        file_meta.MediaStorageSOPInstanceUID = media_storage_sop_instance_uid
        file_meta.FileMetaInformationVersion = file_meta_information_version
        file_meta.ImplementationClassUID = implementation_class_uid
        file_meta.ImplementationVersionName = implementation_version_name
        file_meta.FileMetaInformationGroupLength = file_meta_information_group_length

        # Create the FileDataset instance (initially no data elements, but file_meta supplied)
        dcm = FileDataset(filename_little_endian, {},
                          file_meta=file_meta, preamble=b"\0" * 128)

    # For each element in the Patient data, add to the DICOM object
    for k, v in base_dict.items():
        dcm = add_data(dcm, k, v, cfg, dict_element='BaseAttributes')

    # Add required elements
    dcm.ContentDate = str(datetime.date.today()).replace('-', '')
    dcm.SOPInstanceUID = media_storage_sop_instance_uid
    dcm.SOPClassUID = media_storage_sop_class_uid

    logging.debug('Completed {} Module'.format(dict_element))
    return dcm, cfg
