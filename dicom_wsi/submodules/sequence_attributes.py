# ignore E501

from pydicom.dataset import Dataset
from pydicom.sequence import Sequence


def build_sequences(dcm, cfg):
    ds1 = Dataset()
    ds1.DimensionIndexPointer = cfg['SequenceAttributes']['DimensionIndexSequence[0]']['DimensionIndexPointer']
    ds1.FunctionalGroupPointer = cfg['SequenceAttributes']['DimensionIndexSequence[0]']['FunctionalGroupPointer']

    ds2 = Dataset()
    ds2.DimensionIndexPointer = cfg['SequenceAttributes']['DimensionIndexSequence[1]']['DimensionIndexPointer']
    ds2.FunctionalGroupPointer = cfg['SequenceAttributes']['DimensionIndexSequence[1]']['FunctionalGroupPointer']
    dcm.DimensionIndexSequence = Sequence([ds1, ds2])
    del ds1, ds2

    ds3 = Dataset()
    ds3.XOffsetInSlideCoordinateSystem = cfg['SequenceAttributes']['TotalPixelMatrixOriginSequence'][
        'XOffsetInSlideCoordinateSystem']
    ds3.YOffsetInSlideCoordinateSystem = cfg['SequenceAttributes']['TotalPixelMatrixOriginSequence'][
        'YOffsetInSlideCoordinateSystem']
    dcm.TotalPixelMatrixOriginSequence = Sequence([ds3])
    del ds3

    ds4 = Dataset()
    ds5 = Dataset()
    ds6 = Dataset()

    # IlluminationTypeCodeSequence
    ds4.CodingSchemeDesignator = \
    cfg['SequenceAttributes']['IlluminationTypeCodeSequence']['OpticalPathSequence']['IlluminationTypeCodeSequence'][
        'CodingSchemeDesignator']
    ds4.CodeMeaning = \
    cfg['SequenceAttributes']['IlluminationTypeCodeSequence']['OpticalPathSequence']['IlluminationTypeCodeSequence'][
        'CodeMeaning']
    ds4.CodeValue = \
    cfg['SequenceAttributes']['IlluminationTypeCodeSequence']['OpticalPathSequence']['IlluminationTypeCodeSequence'][
        'CodeValue']

    # IlluminationColorCodeSequence
    ds5.CodingSchemeDesignator = \
    cfg['SequenceAttributes']['IlluminationTypeCodeSequence']['OpticalPathSequence']['IlluminationColorCodeSequence'][
        'CodingSchemeDesignator']
    ds5.CodeMeaning = \
    cfg['SequenceAttributes']['IlluminationTypeCodeSequence']['OpticalPathSequence']['IlluminationColorCodeSequence'][
        'CodeMeaning']
    ds5.CodeValue = \
    cfg['SequenceAttributes']['IlluminationTypeCodeSequence']['OpticalPathSequence']['IlluminationColorCodeSequence'][
        'CodeValue']

    ds7 = Dataset()
    ds7.IlluminationTypeCodeSequence = Sequence([ds4])
    ds8 = Dataset()
    ds8.IlluminationColorCodeSequence = Sequence([ds5])
    ds8.OpticalPathIdentifier = cfg['SequenceAttributes']['IlluminationTypeCodeSequence']['OpticalPathSequence'][
        'OpticalPathIdentifier']
    ds8.OpticalPathDescription = cfg['SequenceAttributes']['IlluminationTypeCodeSequence']['OpticalPathSequence'][
        'OpticalPathDescription']

    ds9 = Dataset()
    ds9.OpticalPathSequence = Sequence([ds8])
    dcm.IlluminationTypeCodeSequence = Sequence([ds9])
    del ds9, ds8, ds7, ds6, ds5, ds4

    return dcm
