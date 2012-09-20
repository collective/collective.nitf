# -*- coding: utf-8 -*-

import unicodedata

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

from five import grok

from plone.registry.interfaces import IRegistry

from collective.nitf import _
from collective.nitf.controlpanel import INITFSettings


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
            token = unicodedata.normalize('NFKD', genre).encode('ascii', 'ignore').lower()
            items.append(SimpleVocabulary.createTerm(genre, token, _(genre)))
        return SimpleVocabulary(items)

grok.global_utility(AvailableGenresVocabulary, name=u'collective.nitf.AvailableGenres')


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
            token = unicodedata.normalize('NFKD', section).encode('ascii', 'ignore').lower()
            items.append(SimpleVocabulary.createTerm(section, token, section))
        return SimpleVocabulary(items)

grok.global_utility(SectionsVocabulary, name=u'collective.nitf.AvailableSections')
