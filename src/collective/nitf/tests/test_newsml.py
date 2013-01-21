# -*- coding: utf-8 -*-

from DateTime import DateTime

import unittest2 as unittest

from zope.component import getUtility

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue

from plone.registry.interfaces import IRegistry

from plone.uuid.interfaces import IUUID

from Products.CMFCore.utils import getToolByName

try:
    from collective.syndication.interfaces import IFeedSettings
    from collective.syndication.interfaces import ISiteSyndicationSettings
    HAS_C_SYNDICATION = True
except:
    HAS_C_SYNDICATION = False

from collective.nitf.testing import INTEGRATION_TESTING


BODY_TEXT = """<p>Test text</p>
<h2>Header</h2>
<p class="one" id="test">New <span>line</span> <span>followed</span> by more text</p>
<a href="http://www.google.com" class="new">Google</a>
<p> This paragraph has a <a href="http://www.google.com" class="new">link</a> inside</p>
<ol><li>one</li><li>two</li></ol>
<ul><li>one</li><li>two</li></ul>
"""


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.wf = getToolByName(self.portal, 'portal_workflow')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

        if HAS_C_SYNDICATION:
            registry = getUtility(IRegistry)
            self.site_settings = registry.forInterface(ISiteSyndicationSettings)
            self.site_settings.allowed = True
            settings = IFeedSettings(self.folder)
            settings.enabled = True
            settings = IFeedSettings(self.n1)
            settings.enabled = True

    def test_newsml_view_for_empty_nitf(self):
        newsml_view = self.n1.restrictedTraverse("newsml.xml")
        feed = newsml_view.feed()
        item = [i for i in feed.items][0]

        self.assertFalse(item.image_url)
        self.assertEqual(item.author, u'')
        self.assertEqual(item.title, u'')
        self.assertEqual(item.description, u'')
        self.assertEqual(item.uid, IUUID(self.n1))
        self.assertEqual(item.modified, DateTime(self.n1.ModificationDate()))
        self.assertEqual(item.body, '')
        self.assertEqual(item.image_title, '')
        self.assertEqual(item.image_mime_type, None)
        self.assertFalse(item.has_image)
        self.assertNotEqual(item.duid(1), item.duid(2))
        self.assertEqual(item.created, self.n1.created())

    def test_newsml_view_for_populated_nitf(self):
        self.n1.setTitle("News Item")
        self.n1.setDescription("News Description")

        self.n1.text = RichTextValue(BODY_TEXT)

        self.n1.invokeFactory('Image', 'img1')
        self.n1.byline = u"test_author"

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.wf.doActionFor(self.n1, 'publish')
        self.wf.notifySuccess(self.n1, 'publish')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

        newsml_view = self.n1.restrictedTraverse("newsml.xml")
        feed = newsml_view.feed()
        item = [i for i in feed.items][0]

        self.assertEqual(item.image_url, 'http://nohost/plone/test-folder/n1/img1/image_large')
        self.assertEqual(item.author, u'test_author')
        self.assertEqual(item.title, 'News Item')
        self.assertEqual(item.description, 'News Description')
        self.assertEqual(item.uid, IUUID(self.n1))
        self.assertEqual(item.modified, DateTime(self.n1.ModificationDate()))

        output = '<p>Test text</p><p>Header</p><p>New line followed by more text</p><a href="http://www.google.com">Google</a><p> This paragraph has a <a href="http://www.google.com">link</a> inside</p><ul><li>one</li><li>two</li></ul><ul><li>one</li><li>two</li></ul>'
        self.assertEqual(item.body, output)

        self.assertTrue(item.has_image)
        self.assertEqual(item.created, self.n1.created())
