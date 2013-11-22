# -*- coding: utf-8 -*-

from collective.nitf.controlpanel import INITFSettings
from collective.nitf.testing import INTEGRATION_TESTING
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(INITFSettings)

    def test_genres_vocabulary(self):
        name = 'collective.nitf.Genres'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util, None)
        genres = util(self.portal)
        self.assertEqual(len(genres), 44)

    def test_available_genres_vocabulary(self):
        name = 'collective.nitf.AvailableGenres'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util, None)
        available_genres = util(self.portal)
        self.assertEqual(len(available_genres), 1)
        self.assertIn(u'Current', available_genres)

    def test_available_genres_vocabulary_is_sorted(self):
        self.settings.available_genres = [u'Voicer', u'Current', u'Actuality']
        name = 'collective.nitf.AvailableGenres'
        util = getUtility(IVocabularyFactory, name)
        genres = util(self.portal)
        genres = [i.title for i in genres]
        self.assertListEqual(genres, [u'Actuality', u'Current', u'Voicer'])

    def test_available_sections_vocabulary(self):
        name = 'collective.nitf.AvailableSections'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util, None)
        sections = util(self.portal)
        self.assertEqual(len(sections), 1)
        self.assertIn(u'General', sections)

    def test_available_sections_vocabulary_is_sorted(self):
        self.settings.available_sections = set([u'5', u'4', u'3', u'2', u'1'])
        name = 'collective.nitf.AvailableSections'
        util = getUtility(IVocabularyFactory, name)
        sections = util(self.portal)
        sections = [i.title for i in sections]
        self.assertListEqual(sections, [u'1', u'2', u'3', u'4', u'5'])

    def test_urgencies_vocabulary(self):
        name = 'collective.nitf.Urgencies'
        util = queryUtility(IVocabularyFactory, name)
        self.assertIsNotNone(util, None)
        urgencies = util(self.portal)
        self.assertEqual(len(urgencies), 3)
