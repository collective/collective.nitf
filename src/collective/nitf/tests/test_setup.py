# -*- coding: utf-8 -*-
from collective.nitf.config import PROJECTNAME
from collective.nitf.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.browser.admin import AddPloneSite
from Products.CMFPlone.interfaces.resources import IBundleRegistry
from Products.CMFPlone.utils import get_installer
from zope.component import getUtility

import unittest


DEPENDENCIES = ()

JS = "++plone++collective.nitf/nitf.js"
CSS = "++plone++collective.nitf/nitf.css"


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.installer = get_installer(self.portal, self.request)
        self.registry = getUtility(IRegistry)
        self.bundles = self.registry.collectionOfInterface(
            IBundleRegistry, prefix="plone.bundles"
        )

    def test_installed(self):
        self.assertTrue(self.installer.is_product_installed(PROJECTNAME))

    def test_dependencies_installed(self):
        for p in DEPENDENCIES:
            self.assertTrue(
                self.installer.isProductInstalled(p), "{0} not installed".format(p)
            )

    def test_setup_permission(self):
        permission = "collective.nitf: Setup"
        roles = self.portal.rolesOfPermission(permission)
        roles = [r["name"] for r in roles if r["selected"]]
        expected = ["Manager", "Site Administrator"]
        self.assertListEqual(roles, expected)

    def test_add_permission(self):
        permission = "collective.nitf: Add News Article"
        roles = self.portal.rolesOfPermission(permission)
        roles = [r["name"] for r in roles if r["selected"]]
        expected = ["Contributor", "Manager", "Owner", "Site Administrator"]
        self.assertListEqual(roles, expected)

    def test_addon_layer(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertIn("INITFLayer", layers)

    def test_link_workflow_changed(self):
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType("Link")
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], "one_state_workflow")

    def test_hide_extensions_profiles(self):
        app = self.layer["app"]
        request = self.layer["request"]
        add_plone_site = AddPloneSite(app, request)
        profiles = add_plone_site.profiles()
        extensions_profiles = profiles["extensions"]
        profiles_ids = [profile["id"] for profile in extensions_profiles]
        nitf_profiles = [
            profile_id
            for profile_id in profiles_ids
            if profile_id.startswith(PROJECTNAME)
        ]
        self.assertEqual([u"collective.nitf:default"], nitf_profiles)

    def test_jsregistry(self):
        bundle = self.bundles["nitf"]
        self.assertEqual(bundle.jscompilation, JS)

    def test_cssregistry(self):
        bundle = self.bundles["nitf"]
        self.assertEqual(bundle.csscompilation, CSS)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.installer = get_installer(self.portal, self.request)
        self.installer.uninstall_product(PROJECTNAME)
        self.registry = getUtility(IRegistry)
        self.bundles = self.registry.collectionOfInterface(
            IBundleRegistry, prefix="plone.bundles"
        )

    def test_uninstalled(self):
        self.assertFalse(self.installer.is_product_installed(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertNotIn("INITFLayer", layers)

    def test_bundle_removed(self):
        self.assertNotIn("nitf", self.bundles.keys())

    # FIXME: https://github.com/collective/collective.nitf/issues/168
    @unittest.expectedFailure
    def test_link_workflow_restored(self):
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType("Link")
        # default binding
        self.assertEqual(len(chain), 0)
