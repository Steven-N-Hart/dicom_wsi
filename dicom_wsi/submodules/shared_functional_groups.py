from pydicom.dataset import Dataset
from pydicom.sequence import Sequence


def build_functional_groups(dcm, cfg):
    ds1 = Dataset()
    ds2 = Dataset()
    ds3 = Dataset()
    ds4 = Dataset()

    ds1.PixelSpacing = ['0.000456024078', '0.000326086971']
    ds1.SliceThickness = 1
    ds2.PixelMeasuresSequence = Sequence([ds1])
    ds3.OpticalPathIdentifier = '1'
    ds4.OpticalPathSequence = Sequence([ds3])
    dcm.SharedFunctionalGroupsSequence = Sequence([ds2, ds4])
    return dcm
