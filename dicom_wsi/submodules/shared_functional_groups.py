from pydicom.dataset import Dataset
from pydicom.sequence import Sequence


def build_functional_groups(dcm, cfg):
    ds1 = Dataset()
    ds2 = Dataset()

    ds1.PixelSpacing = ['0.000456024078', '0.000326086971']  # TODO: Do not hard-code
    ds1.SliceThickness = 1
    ds2.PixelMeasuresSequence = Sequence([ds1])

    ds3 = Dataset()
    ds3.OpticalPathIdentifier = '1'
    ds2.OpticalPathIdentificationSequence = Sequence([ds3])

    ds4 = Dataset()
    ds4.FrameType = ['ORIGINAL', 'PRIMARY', 'VOLUME', 'NONE']  # TODO: Do not hard-code
    ds2.WholeSlideMicroscopyImageFrameTypeSequence = Sequence([ds4])
    dcm.SharedFunctionalGroupsSequence = Sequence([ds2])

    del ds1, ds2, ds3
    return dcm
