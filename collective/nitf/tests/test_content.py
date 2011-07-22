# -*- coding: utf-8 -*-

"""
$Id: test_content.py 242547 2011-07-19 01:05:39Z hvelarde $
"""

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.textfield.value import RichTextValue
from plone.dexterity.interfaces import IDexterityFTI

from collective.nitf.content import INITF
from collective.nitf.testing import INTEGRATION_TESTING


class TestNITFIntegration(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

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

    def test_subtitle_indexed(self):
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.folder['n1']
        n1.subtitle = 'The subtitle'
        n1.reindexObject()
        result = self.portal.portal_catalog(subtitle='The subtitle')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())

    def test_byline_indexed(self):
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.folder['n1']
        n1.byline = 'Author'
        n1.reindexObject()
        result = self.portal.portal_catalog(byline='Author')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())

    def test_kind_indexed(self):
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.folder['n1']
        n1.kind = 'News Type'
        n1.reindexObject()
        result = self.portal.portal_catalog(kind='News Type')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())

    def test_section_indexed(self):
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.folder['n1']
        n1.section = 'Section'
        n1.reindexObject()
        result = self.portal.portal_catalog(section='Section')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())

    def test_urgency_indexed(self):
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.folder['n1']
        n1.urgency = '5'
        n1.reindexObject()
        result = self.portal.portal_catalog(urgency='5')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())

    def test_searchable_text_indexed(self):
        """SearchableText must contain id, title, subtitle, abstract, author
        and body text as plain text.
        """
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        n1 = self.folder['n1']
        n1.title = 'The title'
        n1.subtitle = 'The subtitle'
        n1.description = 'Abstract'
        n1.byline = 'Author'
        n1.text = RichTextValue('Body text', 'text/plain', 'text/html')
        n1.reindexObject()
        result = self.portal.portal_catalog(SearchableText='n1')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())
        result = self.portal.portal_catalog(SearchableText='The title')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())
        result = self.portal.portal_catalog(SearchableText='The subtitle')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())
        result = self.portal.portal_catalog(SearchableText='Abstract')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())
        result = self.portal.portal_catalog(SearchableText='Author')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())
        result = self.portal.portal_catalog(SearchableText='Body text')
        self.assertEquals(1, len(result))
        self.assertEquals(result[0].getURL(), n1.absolute_url())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
