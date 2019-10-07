import logging
from utils import uid_maker, make_time, make_date
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence

def build_study(dcm, study_dict):
    logging.debug('Beginning Study Module')

    if study_dict is '':
        return dcm

    ds1 = Dataset()

    if study_dict.get('StudyInstanceUID'):
        dcm.StudyInstanceUID = uid_maker('StudyInstanceUID', study_dict['StudyInstanceUID'])

    dcm.StudyTime = make_time(study_dict.get('StudyTime'))
    dcm.StudyDate = make_date(study_dict.get('StudyDate'))

    if study_dict.get('StudyID'):
        dcm.StudyInstanceUID = uid_maker('StudyID', study_dict['StudyID'])

    if study_dict.get('StudyID'):
        dcm.StudyID = study_dict['StudyID']
    if study_dict.get('StudyDescription'):
        dcm.StudyDescription = study_dict['StudyDescription']
    if study_dict.get('ReferringPhysicianName'):
        dcm.ReferringPhysicianName = study_dict['ReferringPhysicianName']
    if study_dict.get('ReferringPhysicianName'):
        dcm.ReferringPhysicianName = study_dict['ReferringPhysicianName']
    if study_dict.get('PhysiciansOfRecord'):
        dcm.PhysiciansOfRecord = study_dict['PhysiciansOfRecord']
    if study_dict.get('NameOfPhysiciansReadingStudy'):
        dcm.NameOfPhysiciansReadingStudy = study_dict['NameOfPhysiciansReadingStudy']
    if study_dict.get('ConsultingPhysicianName'):
        dcm.ConsultingPhysicianName = study_dict['ConsultingPhysicianName']
    if study_dict.get('AccessionNumber'):
        dcm.AccessionNumber = study_dict['AccessionNumber']

    if study_dict.get('IssuerOfAccessionNumberSequence') and study_dict.get('LocalNamespaceEntityID'):
        ds1.LocalNamespaceEntityID = study_dict['LocalNamespaceEntityID']
        dcm.IssuerOfAccessionNumberSequence = Sequence([ds1])

    logging.debug('Completed Study Module')
    return dcm
