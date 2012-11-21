# -*- coding: utf-8 -*-
from collective.nitf import _
from collective.nitf.config import GENRES
from collective.nitf.config import URGENCIES
from collective.nitf.controlpanel import INITFSettings
from five import grok
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

import unicodedata


def _normalize_token(token):
    ''' Normalize a token using ascii as encoding '''
    normalize = unicodedata.normalize
    return normalize('NFKD', token).encode('ascii', 'ignore').lower()


class AvailableGenresVocabulary(object):
    """ Creates a vocabulary with the available genres stored in the registry;
    the vocabulary is normalized to allow the use of non-ASCII characters.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
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

grok.global_utility(AvailableGenresVocabulary,
                    name=u'collective.nitf.AvailableGenres')


class SectionsVocabulary(object):
    """ Creates a vocabulary with the available sections stored in the
    registry; the vocabulary is normalized to allow the use of non-ASCII
    characters.
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFSettings)
        available_sections = list(settings.available_sections)
        available_sections.sort()
        items = []
        for section in available_sections:
            token = _normalize_token(section)
            items.append(SimpleVocabulary.createTerm(section, token, section))
        return SimpleVocabulary(items)

grok.global_utility(SectionsVocabulary,
                    name=u'collective.nitf.AvailableSections')


class GenresVocabulary(object):
    """ Creates a vocabulary to expose Genres
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        return GENRES

grok.global_utility(GenresVocabulary, name=u'collective.nitf.Genres')


class UrgenciesVocabulary(object):
    """ Creates a vocabulary to expose Urgencies
    """
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        return URGENCIES

grok.global_utility(UrgenciesVocabulary, name=u'collective.nitf.Urgencies')
