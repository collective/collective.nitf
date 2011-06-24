# -*- coding: utf-8 -*-

import unittest

from zope.component import createObject
from zope.component import queryUtility

from Products.PloneTestCase.ptc import PloneTestCase
from Products.CMFPlone.utils import getToolByName
from plone.dexterity.interfaces import IDexterityFTI

from collective.transmogrifier.transmogrifier import Transmogrifier
from collective.nitf.tests.layer import MigrationLayer


class TestNITFIntegration(PloneTestCase):

    layer = MigrationLayer

    def test_transmogrify(self):
        transmogrifier = Transmogrifier(self.portal)
        transmogrifier("nitfmigrator")
        catalog = getToolByName(self.portal, 'portal_catalog')
        results = catalog({'Type': u'NITF',},)
        out = []
        for result in results:
            out.append((result['id'], result['Title']))
        self.assertEqual(len(out), 4)



    def test_migrate_dry_run(self):
        """
        news_1 = self.folder.n1.portal_type, self.folder.n1.getId(), \
                  self.folder.n1.Title()
        self.assertEqual(news_1, ('News Item', 'n1', 'News 1'))
        transmogrifier = Transmogrifier(self.portal)
        """


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
