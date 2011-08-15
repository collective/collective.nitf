# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from collective.nitf import config
from collective.nitf.testing import INTEGRATION_TESTING

TYPES = (
    'collective.nitf.content',
    )

JS = (
    '++resource++collective.nitf/jquery.tools.min.js',
    )


class TestInstall(unittest.TestCase):
    """ensure product is properly installed"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.failUnless(qi.isProductInstalled(config.PROJECTNAME),
                            '%s not installed' % config.PROJECTNAME)

    def test_types(self):
        portal_types = getattr(self.portal, 'portal_types')
        for t in TYPES:
            self.failUnless(t in portal_types.objectIds(),
                            '%s content type not installed' % t)

    def test_javascripts(self):
        portal_js = getattr(self.portal, 'portal_javascripts')
        for js in JS:
            self.failUnless(js in portal_js.getResourceIds(),
                            '%s javascript not installed' % js)


class TestUninstall(unittest.TestCase):
    """ensure product is properly uninstalled"""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[config.PROJECTNAME])

    def test_uninstalled(self):
        self.failIf(self.qi.isProductInstalled(config.PROJECTNAME))

    def test_types(self):
        portal_types = getattr(self.portal, 'portal_types')
        for t in TYPES:
            self.failIf(t in portal_types.objectIds(),
                        '%s content type not uninstalled' % t)

    def test_javascripts(self):
        portal_js = getattr(self.portal, 'portal_javascripts')
        for js in JS:
            self.failIf(js in portal_js.getResourceIds(),
                        '%s javascript not uninstalled' % js)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
