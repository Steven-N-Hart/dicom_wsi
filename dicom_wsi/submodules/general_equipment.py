import logging

def build_equipment(dcm, equip_dict):
    logging.debug('Beginning Equipment Module')

    if equip_dict is '':
        return dcm

    if equip_dict.get('PixelPaddingValue'):
        dcm.PixelPaddingValue = equip_dict['PixelPaddingValue']

    logging.debug('Completed Equipment Module')
    return dcm
