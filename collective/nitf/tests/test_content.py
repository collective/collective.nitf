# -*- coding: utf-8 -*-

"""
$Id$
"""

import unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.dexterity.interfaces import IDexterityFTI

from Products.PloneTestCase.ptc import PloneTestCase
from collective.nitf.tests.layer import Layer

from collective.nitf.content import INITF


class TestNITFIntegration(PloneTestCase):

    layer = Layer

    def test_adding(self):
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.folder['n1']
        self.failUnless(INITF.providedBy(n1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        schema = fti.lookupSchema()
        self.assertEquals(INITF, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.nitf.content')
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(INITF.providedBy(new_object))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
