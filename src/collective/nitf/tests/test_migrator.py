# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from Products.CMFPlone.utils import getToolByName
from plone.dexterity.interfaces import IDexterityFTI

from collective.transmogrifier.transmogrifier import Transmogrifier
from collective.nitf.testing import INTEGRATION_TESTING


class TestNITFIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def test_transmogrify(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        results = catalog({'portal_type': u'collective.nitf.content', }, )
        self.assertEqual(len(results), 0)
        transmogrifier = Transmogrifier(portal)
        transmogrifier("nitfmigrator")
        results = catalog({'portal_type': u'collective.nitf.content', }, )
        self.assertEqual(len(results), 4)

    def test_migrate_dry_run(self):
        pass


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
