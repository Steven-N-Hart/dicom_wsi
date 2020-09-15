"""Console script for dicom_wsi."""
import argparse
import sys
import logging
import pydicom


def extract_ann_dicom(dicom_file):
    '''Pydicom help:https://pydicom.github.io/pydicom/stable/old/getting_started.html'''
    '''Pydicom object from input dicome file'''
    ds = pydicom.dcmread(dicom_file)

    '''Explore dicom object iteratively'''
    #ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[0].dir()

    '''dictionary object for all regions'''
    dict_annotations={}

    '''Checking if the dicom file have annotations'''
    if 'GraphicAnnotationSequence' in ds and len(ds.GraphicAnnotationSequence)>0 and 'ReferencedImageSequence' in ds.GraphicAnnotationSequence[0] and len(ds.GraphicAnnotationSequence[0].ReferencedImageSequence)>0 and 'GraphicObjectSequence' in ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0]:
        '''Number of regions in the annotation'''
        dict_annotations['Num_Regions']=len(ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence)

        '''Empty list for regions'''
        dict_annotations['Regions']=[]

        '''Extract each region'''
        for i in range(0,dict_annotations['Num_Regions']):
            dict_Region={}
            dict_Region['GeoShape'] = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].GraphicType
            dict_Region['Id'] = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].GraphicGroupID
            list_tmp = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].UnformattedTextValue.split("_")
            assert(len(list_tmp) >= 2)
            dict_Region['Text'] = list_tmp[0]
            dict_Region['GeoShape'] = list_tmp[1]

            if dict_Region['GeoShape'] == 'Points':
                dict_Region['Vertices'] = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].GraphicData

            if dict_Region['GeoShape'] == 'Rectangle':
                x2 = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].BoundingBoxBottomRightHandCorner[0]
                y1 = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].BoundingBoxBottomRightHandCorner[1]
                x1 = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].BoundingBoxTopLeftHandCorner[0]
                y2 = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].BoundingBoxTopLeftHandCorner[1]
                dict_Region['Vertices'] = [x1,y1,x2,y1,x1,y2,x2,y2]

            if dict_Region['GeoShape'] == 'Ellipse':
                dict_Region['Vertices'] = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].GraphicData

            if dict_Region['GeoShape'] == 'Area' or dict_Region['GeoShape'] == 'Polygon':
                dict_Region['Vertices'] = ds.GraphicAnnotationSequence[0].ReferencedImageSequence[0].GraphicObjectSequence[i].GraphicData

            dict_annotations['Regions'].append(dict_Region)

    return dict_annotations

def main():
    """Extract annotations script for dicom_wsi."""
    parser = argparse.ArgumentParser()

    parser.add_argument("-D", "--dicom", dest='dicom', required=True, help="DICOM file")

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

    '''Extract annotations from dicom'''
    dict_annotations = extract_ann_dicom(dicom_file)
    print(dict_annotations)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
