# ignore E501

from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from pydicom.tag import Tag


def build_sequences(dcm, cfg):
    ds1 = Dataset()
    ds1.DimensionOrganizationUID = '1.2.276.0.7230010.3.1.4.8323329.25650.1570640401.346049'
    # ds1.DimensionIndexPointer = dcm.ColumnPositionInTotalImagePixelMatrix
    # ds1.FunctionalGroupPointer = dcm.PlanePositionSlideSequence
    ds1.DimensionIndexPointer = Tag(0x0048021E)
    ds1.FunctionalGroupPointer = Tag(0x0048021A)

    ds2 = Dataset()
    ds2.DimensionOrganizationUID = '1.2.276.0.7230010.3.1.4.8323329.25650.1570640401.346049'
    # ds2.DimensionIndexPointer = dcm.RowPositionInTotalImagePixelMatrix
    # ds2.FunctionalGroupPointer = dcm.PlanePositionSlideSequence
    ds2.DimensionIndexPointer = Tag(0x0048021F)
    ds2.FunctionalGroupPointer = Tag(0x0048021A)

    # Delete the tem storage variable
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
    ds4.CodingSchemeDesignator = cfg.get('SequenceAttributes').get('IlluminationTypeCodeSequence').get(
        'OpticalPathSequence').get('IlluminationTypeCodeSequence').get('CodingSchemeDesignator')
    ds4.CodeMeaning = cfg.get('SequenceAttributes').get('IlluminationTypeCodeSequence').get('OpticalPathSequence').get(
        'IlluminationTypeCodeSequence').get('CodeMeaning')
    ds4.CodeValue = cfg.get('SequenceAttributes').get('IlluminationTypeCodeSequence').get('OpticalPathSequence').get(
        'IlluminationTypeCodeSequence').get('CodeValue')

    # IlluminationColorCodeSequence
    ds5.CodingSchemeDesignator = cfg.get('SequenceAttributes').get('IlluminationTypeCodeSequence').get(
        'OpticalPathSequence').get(
        'IlluminationColorCodeSequence').get('CodingSchemeDesignator')
    ds5.CodeMeaning = cfg.get('SequenceAttributes').get('IlluminationTypeCodeSequence').get('OpticalPathSequence').get(
        'IlluminationColorCodeSequence').get('CodeMeaning')
    ds5.CodeValue = cfg.get('SequenceAttributes').get('IlluminationTypeCodeSequence').get('OpticalPathSequence').get(
        'IlluminationColorCodeSequence').get('CodeValue')

    ds7 = Dataset()
    ds7.IlluminationTypeCodeSequence = Sequence([ds4])

    ds8 = Dataset()
    ds8.IlluminationColorCodeSequence = Sequence([ds5])
    ds8.OpticalPathIdentifier = cfg.get('SequenceAttributes').get('IlluminationTypeCodeSequence').get(
        'OpticalPathSequence').get(
        'OpticalPathIdentifier')
    ds8.OpticalPathDescription = cfg.get('SequenceAttributes').get('IlluminationTypeCodeSequence').get(
        'OpticalPathSequence').get(
        'OpticalPathDescription')

    ds9 = Dataset()
    ds9.OpticalPathSequence = Sequence([ds8])
    dcm.IlluminationTypeCodeSequence = Sequence([ds9])
    del ds9, ds8, ds7, ds6, ds5, ds4

    return dcm
