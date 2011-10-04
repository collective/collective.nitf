# -*- coding: utf-8 -*-

import unittest2 as unittest

from AccessControl import Unauthorized

from zope.interface import directlyProvides

from plone.app.testing import TEST_USER_ID
from plone.app.testing import logout
from plone.app.testing import setRoles

from collective.nitf.interfaces import INITFBrowserLayer
from collective.nitf.testing import INTEGRATION_TESTING


class ActionsTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        directlyProvides(self.request, INITFBrowserLayer)

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']

    def test_registered_actions(self):
        # TODO: implement test
        pass

    def test_organize(self):
        name = '@@organize'
        try:
            self.n1.unrestrictedTraverse(name)
        except AttributeError:
            self.fail('%s has no view %s' % (self.n1, name))

        # action can not be accessed by anonymous users
        logout()
        self.assertRaises(Unauthorized, self.n1.restrictedTraverse, name)

    def test_media_uploader(self):
        name = '@@media_uploader'
        try:
            self.n1.unrestrictedTraverse(name)
        except AttributeError:
            self.fail('%s has no view %s' % (self.n1, name))

        # action can not be accessed by anonymous users
        logout()
        self.assertRaises(Unauthorized, self.n1.restrictedTraverse, name)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
