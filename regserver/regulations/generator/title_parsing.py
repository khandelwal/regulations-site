#vim: set fileencoding=utf-8
import re


def appendix_supplement(data):
    """Handle items pointing to an appendix or supplement"""
    if len(data['index']) == 2 and data['index'][1].isalpha():
        element = {}
        if data['index'][1] == 'Interp':
            element['is_supplement'] = True
        else:
            element['is_appendix'] = True

        segments = try_split(data['title'], (u'—', '-'))
        if segments:
            element['label'], element['sub_label'] = segments
        element['section_id'] = '-'.join(data['index'])
        return element


def try_split(text, chars):
    """Utility method for splitting a string by one of multiple chars"""
    for c in chars:
        segments = text.split(c)
        if len(segments) > 1:
            return [s.strip() for s in segments]


def section(data):
    """ Parse out parts of a section title. """
    if len(data['index']) == 2 and data['index'][1].isdigit():
        element = {}
        element['is_section'] = True
        element['label'] = '.'.join(data['index'])
        element['section_id'] = '-'.join(data['index'])
        element['sub_label'] = re.search(
            element['label'] + r'[^\w]*(.*)', data['title']).group(1)
        return element
