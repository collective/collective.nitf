# -*- coding: utf-8 -*-

import unittest

from zope.component import createObject
from zope.component import queryUtility

from Products.PloneTestCase.ptc import PloneTestCase
from plone.dexterity.interfaces import IDexterityFTI
from collective.transmogrifier.transmogrifier import Transmogrifier

from collective.nitf.tests.layer import MigrationLayer


class TestNITFIntegration(PloneTestCase):

    layer = MigrationLayer

    def test_transmogrify(self):
        transmogrifier = Transmogrifier(self.portal)
        transmogrifier("nitfmigrator")
        print transmogrifier("nitfmigrator")

    def test_migrate_dry_run(self):
        """
        news_1 = self.folder.n1.portal_type, self.folder.n1.getId(), \
                  self.folder.n1.Title()
        self.assertEqual(news_1, ('News Item', 'n1', 'News 1'))
        transmogrifier = Transmogrifier(self.portal)
        """

    def test_migrate(self):
        """
        news_1 = self.folder.n1.portal_type, self.folder.n1.getId(), \
                  self.folder.n1.Title()
        self.assertEqual(news_1, ('News Item', 'n1', 'News 1'))
        migrate_to_nitf(self.folder.n1)
        nitf_1 = self.folder.n1.portal_type, self.folder.n1.getId(), \
                  self.folder.n1.Title()
        self.assertEqual(nitf_1, ('collective.nitf.content', 'n1', 'News 1'))
        """


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
