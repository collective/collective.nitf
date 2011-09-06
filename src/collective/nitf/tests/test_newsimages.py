# -*- coding: utf-8 -*-

import unittest2 as unittest
from StringIO import StringIO

from zope.component import createObject
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import directlyProvides
from zope.publisher.browser import TestRequest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing.z2 import Browser
from plone.app.textfield.value import RichTextValue
from Products.ATContentTypes.interfaces import IImageContent
from Products.CMFPlone.utils import getToolByName
from plone.dexterity.interfaces import IDexterityFTI

from collective.transmogrifier.transmogrifier import Transmogrifier
from collective.nitf.browser import INITFBrowserLayer
from collective.nitf.browser import MediaViewlet
from collective.nitf.browser import MediaLinksViewlet
from collective.nitf.content import INITF
from collective.nitf.testing import INTEGRATION_TESTING

zptlogo = (
    'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
    '\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
    '\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
    '\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
    '\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
    '\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
    '\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
    '\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
    '\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
    '\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
    '\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
    '\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
    '\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
    '\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
    '\x00A\x00;'
    )


class TestNITFNewsAdapter(unittest.TestCase):
    """ The tests begin with 4 NITF News Articles in the user's folder,
        self.folder. Each article has 2 Images, and the views should """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFBrowserLayer)
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.folder['n1'].title = u"Test NITF Article"
        self.add_image(self.folder['n1'], 'news-image-1')
        self.add_image(self.folder['n1'], 'news-image-2')
        self.folder['n1'].reindexObject()
        self.nitf = self.folder['n1']

    def add_image(self, container, m_id):
        container.invokeFactory('Image', id=m_id, title=u"Logo GIF",
                                image=StringIO(zptlogo))
        container[m_id].reindexObject()

    def test_image_content(self):
        adapter = IImageContent(self.nitf)
        self.assertNotEquals(adapter, None)
        self.assertEquals(adapter.getImage(), self.nitf['news-image-1'])


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
