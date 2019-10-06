import re

INT_LIST = ['DA', 'UL', 'US']
TIME_LIST = ['TM']
SIGNEDINT_LIST = ['US or SS']
INTSTRING_LIST = ['IS']
DT_LIST = ['DT']
DS_LIST = ['DS']
CS_LIST = ['CS']

restricted_inputs = {
    'PatientSex': ['M', 'F', 'O'],
    'Modality': ['SM'],
    'BurnedInAnnotation': ['YES', 'NO'],
    'LossyImageCompression': ['00', '01'],
    'PhotometricInterpretation': ['MONOCHROME1', 'RGB', 'YBR_FULL_422', 'YBR_ICT', 'YBR_RCT'],
    'VolumetricProperties': ['VOLUME', 'MIXED', 'SAMPLED', 'DISTORTED'],
    'PositionReferenceIndicator': ['SLIDE_CORNER'],
    'FrameType': ['ORIGINAL, PRIMARY, VOLUME, NONE', 'DERIVED, PRIMARY, VOLUME, RESAMPLED',
                  'DERIVED, PRIMARY, LOCALIZER, RESAMPLED', 'ORIGINAL, PRIMARY, LABEL, NONE'],
}

required_fields = {
    'General': ['OutFile', 'NumberOfLevels'],
    'Patient': [],
    'Specimen': ['ValueType', 'ContainerIdentifier', 'SpecimenIdentifier', 'ConceptNameCodeSequence',
                 'SpecimenDescriptionSequence', 'SpecimenPreparationStepContentItemSequence', 'SpecimenUID'],
    'GeneralStudy': ['StudyInstanceUID'],
    'GeneralSeries': ['Modality', 'SeriesInstanceUID'],
    'GeneralEquipment': [],
    'EnhancedGeneralEquipment': ['DeviceSerialNumber', 'Manufacturer', 'ManufacturerModelName', 'SoftwareVersions'],
    'WholeSlideMicroscopyImage': ['BurnedInAnnotation', 'ExtendedDepthOfField', 'FocusMethod', 'ImageType',
                                  'LossyImageCompression', 'PhotometricInterpretation', 'SpecimenLabelInImage',
                                  'VolumetricProperties', 'ImageOrientationSlide', 'XOffsetInSlideCoordinateSystem',
                                  'YOffsetInSlideCoordinateSystem', 'AcquisitionDateTime', 'AcquisitionDuration',
                                  'ImagedVolumeDepth', 'ImagedVolumeHeight', 'ImagedVolumeWidth',
                                  'TotalPixelMatrixOriginSequence', 'TotalPixelMatrixColumns', 'TotalPixelMatrixRows',
                                  'BitsAllocated', 'BitsStored', 'Columns', 'HighBit', 'PixelRepresentation', 'Rows',
                                  'SamplesPerPixel'],
    'AcquisitionContext': [],
    'FrameOfReference': ['FrameOfReferenceUID'],
    'OpticalPath': ['OpticalPathIdentifier', 'OpticalPathSequence'],
    'SOPCommon': ['SOPClassUID', 'SOPInstanceUID'],
    'ImagePixel': ['PixelData'],
    'MultiFrameFunctionalGroups': ['DimensionIndexPointer', 'FrameType', 'ContentDate', 'InstanceNumber',
                                   'NumberOfFrames', 'DimensionIndexSequence', 'DimensionOrganizationSequence',
                                   'PixelMeasuresSequence', 'SharedFunctionalGroupsSequence',
                                   'WholeSlideMicroscopyImageFrameTypeSequence', 'ContentTime',
                                   'DimensionOrganizationUID']
}

size_limits = {
    '2': ['PixelPaddingValue', 'BitsAllocated', 'BitsStored', 'Columns', 'HighBit', 'PixelRepresentation', 'Rows',
          'SamplesPerPixel', 'PlanarConfiguration', 'InConcatenationNumber'],
    '4': ['ImagedVolumeDepth', 'ImagedVolumeHeight', 'ImagedVolumeWidth', 'TotalPixelMatrixColumns',
          'TotalPixelMatrixRows', 'TotalPixelMatrixFocalPlanes', 'NumberOfOpticalPaths', 'DimensionIndexPointer',
          'FunctionalGroupPointer', 'ConcatenationFrameOffsetNumber'],
    '8': ['PatientBirthDate', 'StudyDate', 'SeriesDate', 'AcquisitionDuration', 'ContentDate'],
    '12': ['SeriesNumber', 'InstanceNumber', 'NumberOfFrames'],
    '16': ['PatientSex', 'ValueType', 'AccessionNumber', 'StudyID', 'StudyTime', 'Modality', 'SeriesTime',
           'BurnedInAnnotation', 'ExtendedDepthOfField', 'FocusMethod', 'ImageType', 'LossyImageCompression',
           'PhotometricInterpretation', 'SpecmenLabelInImage', 'VolumetricProperties', 'LossyImageCompressionMethod',
           'ImageOrientationSlide', 'XOffsetInSlideCoordinateSystem', 'YOffsetInSlideCoordinateSystem',
           'LossyImageCompressionRatio', 'ObjectiveLensPower', 'OpticalPathIdentifier', 'FrameType',
           'DimensionOrganizationType', 'PixelSpacing', 'SliceThickness', 'ContentTime'],
    '26': ['AcquisitionDateTime'],
    '64': ['PatientID', 'PatientName', 'ContainerIdentifier', 'SpecimenIdentifier', 'SpecimenShortDescription',
           'SpecimenUID', 'StudyDescription', 'ReferringPhysicianName', 'ConsultingPhysicianName',
           'NameOfPhysiciansReadingStudy', 'PhysiciansOfRecord', 'StudyInstanceUID', 'SeriesDescription',
           'OperatorsName', 'SeriesInstanceUID', 'DeviceSerialNumber', 'Manufacturer', 'ManufacturerModelName',
           'SoftwareVersions', 'PositionReferenceIndicator', 'FrameOfReferenceUID', 'SOPClassUID', 'SOPInstanceUID',
           'DimensionDescriptionLabel', 'DimensionOrganizationUID', 'ConcatenationUID',
           'SOPInstanceUIDOfConcatenationSource']
}

def cs_validator(key, value):
    assert re.sub('[a-zA-Z _]', '', value).__len__() == 0, \
        "{} must only contain a-z, A-Z, space, or _, but your provided {}".format(key, value)

def int_validator(key, value):
    assert re.sub('[0-9]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, but your provided {}".format(key, value)

def signedint_validator(key, value):
    assert re.sub('[0-9-]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9 and -, but your provided {}".format(key, value)

def time_validator(key, value):
    assert re.sub('[0-9 .]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, space and ., but your provided {}".format(key, value)

def ui_validator(key, value):
    assert re.sub('[0-9.]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9 and ., but your provided {}".format(key, value)

def dt_validator(key, value):
    assert re.sub('[0-9+-. ]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, +, -, space, and ., but your provided {}".format(key, value)

def ds_validator(key, value):
    assert re.sub('[0-9+-eE]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, +, -, e, and E, but your provided {}".format(key, value)

def intstring_validator(key, value):
    assert re.sub('[0-9+-]', '', str(value)).__len__() == 0, \
        "{} must only contain 0-9, +, and - but your provided {}".format(key, value)
