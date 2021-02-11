"""Console script for dicom_wsi."""
import argparse
import sys
import logging
import pydicom
import os
from PIL import Image

def extract_imagepatches_dicom(dicom_file, image_dir):
    '''Pydicom help:https://pydicom.github.io/pydicom/stable/old/getting_started.html'''
    '''Pydicom object from input DICOM file'''

    ds = pydicom.dcmread(dicom_file)

    '''checking if PerFrameFunctionalGroupsSequence in ds'''

    if 'PerFrameFunctionalGroupsSequence' in ds:
        for i in range(0,len(ds.PerFrameFunctionalGroupsSequence)):
            '''Getting image coordinates'''
            y=str(ds.PerFrameFunctionalGroupsSequence[i].PlanePositionSlideSequence[0].RowPositionInTotalImagePixelMatrix)
            x=str(ds.PerFrameFunctionalGroupsSequence[i].PlanePositionSlideSequence[0].ColumnPositionInTotalImagePixelMatrix)
            XOffset=str(ds.PerFrameFunctionalGroupsSequence[i].PlanePositionSlideSequence[0].XOffsetInSlideCoordinateSystem)
            YOffset=str(ds.PerFrameFunctionalGroupsSequence[i].PlanePositionSlideSequence[0].YOffsetInSlideCoordinateSystem)
            img_name =  os.path.join(image_dir,x+'_'+y+'_'+XOffset+'_'+YOffset+'.png')

            '''Gettng image content'''
            ds.convert_pixel_data()
            img = Image.fromarray(ds.pixel_array[i],'RGB')
            img.save(img_name, "PNG")




def main():
    """Extract annotations script for dicom_wsi."""
    parser = argparse.ArgumentParser()

    parser.add_argument("-D", "--dicom", dest='dicom', required=True, help="DICOM file")
    parser.add_argument("-d", "--image_dir", dest='image_dir', required=True, help="OUTPUT Image directory")

    '''Create Looger'''
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    '''reading the config filename'''
    arg = parser.parse_args()

    '''printing the config param'''
    logger.info("Entered Dicom file " + arg.dicom)

    '''Input Dicom file'''
    dicom_file = arg.dicom
    image_dir = arg.image_dir
    if not os.path.exists(image_dir):
        logger.info(f'Creating {image_dir}')
        os.mkdir(image_dir)

    '''Extract image patches'''
    extract_imagepatches_dicom(dicom_file,image_dir)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
