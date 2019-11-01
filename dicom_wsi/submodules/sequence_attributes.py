# ignore E501

from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
from pydicom.tag import Tag
from pydicom.uid import generate_uid

def build_sequences(dcm, cfg):
    ds0 = Dataset()
    ds0.DimensionOrganizationUID = '1.2.276.0.7230010.3.1.4.8323329.17698.1572316846.287083'
    dcm.DimensionOrganizationSequence = Sequence([ds0])
    del ds0

    ds1 = Dataset()
    ds1.DimensionOrganizationUID = '1.2.276.0.7230010.3.1.4.8323329.17698.1572316846.287083'
    ds1.DimensionIndexPointer = Tag(0x0048021E)
    ds1.FunctionalGroupPointer = Tag(0x0048021A)

    ds2 = Dataset()
    ds2.DimensionOrganizationUID = '1.2.276.0.7230010.3.1.4.8323329.17698.1572316846.287083'
    ds2.DimensionIndexPointer = Tag(0x0048021F)
    ds2.FunctionalGroupPointer = Tag(0x0048021A)

    dcm.DimensionIndexSequence = Sequence([ds1, ds2])
    del ds1, ds2

    ds3 = Dataset()
    ds3.XOffsetInSlideCoordinateSystem = 20
    ds3.YOffsetInSlideCoordinateSystem = 40
    dcm.TotalPixelMatrixOriginSequence = Sequence([ds3])
    del ds3

    ds4 = Dataset()
    ds5 = Dataset()

    # IlluminationTypeCodeSequence
    ds4.CodingSchemeDesignator = 'DCM'
    ds4.CodeMeaning = 'Brightfield illumination'
    ds4.CodeValue = '111744'

    # IlluminationColorCodeSequence
    ds5.CodingSchemeDesignator = 'DCM'
    ds5.CodeMeaning = 'No filter'
    ds5.CodeValue = '111609'

    ds7 = Dataset()
    ds7.IlluminationTypeCodeSequence = Sequence([ds4])
    ds7.IlluminationColorCodeSequence = Sequence([ds5])
    ds7.OpticalPathIdentifier = '1'
    ds7.OpticalPathDescription = 'Brightfield'

    dcm.OpticalPathSequence = Sequence([ds7])
    del ds7, ds5, ds4

    dcm.AcquisitionContextSequence = Sequence([])

    ds0 = Dataset()
    ds0.LocalNamespaceEntityID = 'UNKNOWN'
    dcm.IssuerOfTheContainerIdentifierSequence = Sequence([ds0])
    del ds0


    ds0 = Dataset()

    ds0.SpecimenIdentifier = 'Unknown'
    ds0.SpecimenPreparationSequence = Sequence([])
    ds0.SpecimenUID = generate_uid(prefix=None)
    ds0.IssuerOfTheSpecimenIdentifierSequence = Sequence([])
    dcm.SpecimenDescriptionSequence = Sequence([ds0])
    dcm.ContainerTypeCodeSequence = Sequence([])
    dcm.ContainerIdentifier = 'Unknown'
    return dcm
