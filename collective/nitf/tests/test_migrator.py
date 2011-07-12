# -*- coding: utf-8 -*-

"""
$Id$
"""

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
        catalog = getToolByName(self.portal, 'portal_catalog')
        results = catalog({'portal_type': u'collective.nitf.content', }, )
        self.assertEqual(len(results), 0)
        transmogrifier = Transmogrifier(self.portal)
        transmogrifier("nitfmigrator")
        results = catalog({'portal_type': u'collective.nitf.content', }, )
        self.assertEqual(len(results), 4)

    def test_migrate_dry_run(self):
        pass


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
