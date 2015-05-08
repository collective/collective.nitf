# -*- coding: utf-8 -*-
from collective.nitf.config import PLONE_VERSION
from collective.nitf.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

if PLONE_VERSION >= '4.3':
    from Products.CMFPlone.interfaces.syndication import IFeed
else:  # 4.2
    from collective.syndication.interfaces import IFeed

import unittest2 as unittest


class NitfItemTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_adapter(self):
        self.n1.byline = 'The Author'
        adapted_folder = IFeed(self.folder)
        adapted_n1 = adapted_folder.items.next()
        self.assertEqual(adapted_n1.author_name, 'The Author')
