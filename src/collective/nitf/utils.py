# -*- coding: utf-8 -*-
"""Functions that will be called when the add form of the content type
is loaded to determine the default values of a field.
"""
from collective.nitf.controlpanel import INITFSettings
from plone import api


def genre_default_value():
    """Return the default value for the genre field as defined in the
    control panel configlet.
    """
    record = INITFSettings.__identifier__ + '.default_genre'
    return api.portal.get_registry_record(record)


def urgency_default_value():
    """Return the default value for the urgency field as defined in
    the control panel configlet.
    """
    record = INITFSettings.__identifier__ + '.default_urgency'
    return api.portal.get_registry_record(record)


def section_default_value():
    """Return the default value for the section field as defined in
    the control panel configlet.
    """
    record = INITFSettings.__identifier__ + '.default_section'
    return api.portal.get_registry_record(record)
