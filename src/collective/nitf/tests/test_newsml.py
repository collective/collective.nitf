# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getUtility

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.registry.interfaces import IRegistry

from plone.uuid.interfaces import IUUID

from collective.syndication.interfaces import IFeedSettings
from collective.syndication.interfaces import ISiteSyndicationSettings

from collective.nitf.testing import INTEGRATION_TESTING


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']
        self.n1.setTitle("News Item")
        
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

    def test_newsml_view_for_nitf_with_image_and_author(self):
        self.n1.invokeFactory('Image', 'img1')
        self.n1.byline = u"test_author"
        
        newsml_view = self.n1.restrictedTraverse("newsml.xml")
        feed = newsml_view.feed()
        item = [i for i in feed.items][0]
        
        self.assertEqual(item.image_url, 'http://nohost/plone/test-folder/n1/img1/image_large')
        self.assertEqual(item.author, u'test_author')
