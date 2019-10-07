import logging

def build_enhanced_equipment(dcm, equip_dict):
    logging.debug('Beginning EnhancedEquipment Module')

    if equip_dict is '':
        return dcm

    if equip_dict.get('DeviceSerialNumber'):
        dcm.DeviceSerialNumber = equip_dict['DeviceSerialNumber']

    if equip_dict.get('Manufacturer'):
        dcm.Manufacturer = equip_dict['Manufacturer']

    if equip_dict.get('ManufacturerModelName'):
        dcm.ManufacturerModelName = equip_dict['ManufacturerModelName']

    if equip_dict.get('SoftwareVersions'):
        dcm.SoftwareVersions = equip_dict['SoftwareVersions']

    logging.debug('Completed EnhancedEquipment Module')
    return dcm
