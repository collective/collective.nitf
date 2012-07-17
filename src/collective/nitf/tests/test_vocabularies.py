# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import queryUtility

from zope.schema.interfaces import IVocabularyFactory

from collective.nitf.testing import INTEGRATION_TESTING


class VocabulariesTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_available_genres_vocabulary(self):
        name = 'collective.nitf.AvailableGenres'
        util = queryUtility(IVocabularyFactory, name)
        self.assertTrue(util is not None)
        available_genres = util(self.portal)
        # FIXME: we need to set up at least one genre
        self.assertEqual(len(available_genres), 0)
        #self.assertTrue(u'Current' in available_genres)

    def test_sections_vocabulary(self):
        name = 'collective.nitf.Sections'
        util = queryUtility(IVocabularyFactory, name)
        self.assertTrue(util is not None)
        sections = util(self.portal)
        # FIXME: we need to set up at least one section
        self.assertEqual(len(sections), 0)
        #self.assertTrue(u'Default' in sections)
