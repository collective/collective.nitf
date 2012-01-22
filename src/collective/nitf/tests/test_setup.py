# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.browserlayer.utils import registered_layers

from collective.nitf.config import PROJECTNAME
from collective.nitf.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):
    """Ensure the NITF package is properly installed.
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_add_permission(self):
        permission = 'collective.nitf: Add News Article'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        self.assertEqual(roles, ['Contributor', 'Manager', 'Owner', 'Site Administrator'])

    def test_browserlayer(self):
        """Browser layers are properly registered at install time.
        """
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('INITFBrowserLayer' in layers,
                        'browser layer not installed')

    def test_link_workflow_changed(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Link', 'obj')
        obj = self.portal['obj']
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType(obj.portal_type)
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'one_state_workflow',
                         'workflow not changed on Link content type')

    def test_javascript_registry(self):
        """JavaScripts are properly registered at install time.
        """
        portal_javascripts = self.portal.portal_javascripts
        self.assertTrue('++resource++collective.nitf/nitf_fixes.js'
            in portal_javascripts.getResourceIds())


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        """Browser layers are properly removed at uninstall time.
        """
        layers = [l.getName() for l in registered_layers()]
        self.assertFalse('INITFBrowserLayer' in layers,
                         'browser layer not removed')

    def test_javascript_registry_removed(self):
        """JavaScripts are properly removed at uninstall time.
        """
        portal_javascripts = self.portal.portal_javascripts
        self.assertTrue('++resource++collective.nitf/nitf_fixes.js'
            not in portal_javascripts.getResourceIds())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
