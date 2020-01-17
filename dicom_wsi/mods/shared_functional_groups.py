from pydicom.dataset import Dataset
from pydicom.sequence import Sequence


def build_functional_groups(dcm, cfg):
    """ all values are hard coded to ensure they are present in the final file """
    ds1 = Dataset()
    ds2 = Dataset()

    pv = cfg.get('OnTheFly').get('PixelSpacing')
    ds1.PixelSpacing = [float(x) for x in pv]
    ds1.SliceThickness = 1
    ds2.PixelMeasuresSequence = Sequence([ds1])

    ds3 = Dataset()
    ds3.OpticalPathIdentifier = '1'
    ds2.OpticalPathIdentificationSequence = Sequence([ds3])

    ds4 = Dataset()
    ds4.FrameType = cfg['BaseAttributes']['ImageType']
    ds2.WholeSlideMicroscopyImageFrameTypeSequence = Sequence([ds4])

    dcm.SharedFunctionalGroupsSequence = Sequence([ds2])

    del ds1, ds2, ds3
    return dcm
