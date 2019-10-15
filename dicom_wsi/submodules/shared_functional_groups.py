from pydicom.dataset import Dataset
from pydicom.sequence import Sequence


def build_functional_groups(dcm, cfg):
    ds1 = Dataset()
    ds2 = Dataset()
    ds3 = Dataset()
    ds1.PixelSpacing = [cfg['SharedFunctionalGroupsSequence']['PixelMeasuresSequence']['PixelSpacing'][0],
                        cfg['SharedFunctionalGroupsSequence']['PixelMeasuresSequence']['PixelSpacing'][1]]
    ds2.PixelMeasuresSequence = Sequence([ds1])
    ds3.InstanceNumber = int(cfg['SharedFunctionalGroupsSequence']['InstanceNumber'])
    ds3.ContentDate = cfg['SharedFunctionalGroupsSequence']['ContentDate']
    ds3.InstanceNumber = int(cfg['SharedFunctionalGroupsSequence']['NumberofFrames'])
    ds3.FrameType = cfg['SharedFunctionalGroupsSequence']['FrameType']
    ds3.SliceThickness = int(cfg['SharedFunctionalGroupsSequence']['SliceThickness'])
    ds3.OpticalPathIdentifier = cfg['SharedFunctionalGroupsSequence']['OpticalPathIdentifier']

    dcm.SharedFunctionalGroupsSequence = Sequence([ds2, ds3])
    return dcm
