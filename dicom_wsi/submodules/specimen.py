import logging
from utils import uid_maker
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence

def build_specimen(dcm, specimen_dict):
    ds1 = Dataset()
    ds2 = Dataset()
    ds3 = Dataset()

    if specimen_dict.get('ContainerIdentifier'):
        dcm.ContainerIdentifier = specimen_dict['ContainerIdentifier']
    if specimen_dict.get('IssuerOfTheContainerIdentifierSequence'):
        dcm.IssuerOfTheContainerIdentifierSequence = specimen_dict['IssuerOfTheContainerIdentifierSequence']

    if specimen_dict.get('SpecimenDescriptionSequence'):

        logging.debug('Processing SpecimenDescriptionSequence')
        if specimen_dict.get('SpecimenIdentifier'):
            ds1.SpecimenIdentifier = specimen_dict['SpecimenIdentifier']
        if specimen_dict.get('IssuerOfTheSpecimenIdentifierSequence'):
            ds1.IssuerOfTheSpecimenIdentifierSequence = specimen_dict['IssuerOfTheSpecimenIdentifierSequence']
        if specimen_dict.get('SpecimenUID'):
            ds1.SpecimenUID = uid_maker('SpecimenUID', specimen_dict['SpecimenUID'])
        if specimen_dict.get('SpecimenTypeCodeSequence'):
            ds1.SpecimenTypeCodeSequence = specimen_dict['SpecimenTypeCodeSequence']
        if specimen_dict.get('SpecimenShortDescription'):
            ds1.SpecimenShortDescription = specimen_dict['SpecimenShortDescription']
        if specimen_dict.get('SpecimenDetailedDescription'):
            ds1.SpecimenDetailedDescription = specimen_dict['SpecimenDetailedDescription']


        if specimen_dict.get('SpecimenPreparationSequence'):

            logging.debug('Processing SpecimenPreparationSequence')
            if specimen_dict.get('ValueType'):
                ds2.ValueType = specimen_dict['ValueType']
            if specimen_dict.get('TextValue'):
                ds2.TextValue = specimen_dict['TextValue']
            ds3.SpecimenPreparationStepContentItemSequence = Sequence([ds2])
            ds1.SpecimenPreparationSequence = Sequence([ds3])

    dcm.SpecimenDescriptionSequence = Sequence([ds1])

    return dcm


