# -*- coding: utf-8 -*-
from collective.nitf import _
from collective.nitf.config import GENRES
from collective.nitf.config import URGENCIES
from collective.nitf.controlpanel import INITFSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary

import unicodedata


# TODO: use plone.i18n normalizer
def _normalize_token(token):
    """Normalize a token using ascii as encoding."""
    normalize = unicodedata.normalize
    return normalize('NFKD', token).encode('ascii', 'ignore').lower()


def AvailableGenresVocabulary(context):
    """ Creates a vocabulary with the available genres stored in the registry;
    the vocabulary is normalized to allow the use of non-ASCII characters.
    """
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    available_genres = list(settings.available_genres)
    # sort by translated genre
    available_genres.sort(lambda a, b: cmp(_(a), _(b)))
    items = []
    for genre in available_genres:
        token = _normalize_token(genre)
        items.append(SimpleVocabulary.createTerm(genre, token, _(genre)))
    return SimpleVocabulary(items)


def SectionsVocabulary(context):
    """ Creates a vocabulary with the available sections stored in the
    registry; the vocabulary is normalized to allow the use of non-ASCII
    characters.
    """
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    available_sections = list(settings.available_sections)
    available_sections.sort()
    items = []
    for section in available_sections:
        token = _normalize_token(section)
        items.append(SimpleVocabulary.createTerm(section, token, section))
    return SimpleVocabulary(items)


def GenresVocabulary(context):
    """ Creates a vocabulary to expose Genres
    """
    return GENRES


def UrgenciesVocabulary(context):
    """ Creates a vocabulary to expose Urgencies
    """
    return URGENCIES
