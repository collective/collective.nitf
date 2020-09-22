# -*- coding: utf-8 -*-
from collective.nitf.config import PROJECTNAME
from collective.nitf.testing import INTEGRATION_TESTING
from collective.nitf.testing import IS_BBB
from collective.nitf.testing import IS_PLONE_5
from collective.nitf.testing import QIBBB
from plone.browserlayer.utils import registered_layers
from Products.CMFPlone.browser.admin import AddPloneSite

import unittest


DEPENDENCIES = (
    'collective.js.jqueryui',
)

JS = '++resource++collective.nitf/nitf.js'
CSS = '++resource++collective.nitf/nitf.css'


class InstallTestCase(unittest.TestCase, QIBBB):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    @unittest.skipIf(IS_BBB, 'Plone >= 5.1')
    def test_installed(self):
        from Products.CMFPlone.utils import get_installer
        qi = get_installer(self.portal, self.request)
        self.assertTrue(qi.is_product_installed(PROJECTNAME))

    @unittest.skipUnless(IS_BBB, 'Plone < 5.1')
    def test_installed_BBB(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_dependencies_installed(self):
        for p in DEPENDENCIES:
            self.assertTrue(
                self.qi.isProductInstalled(p), '{0} not installed'.format(p))

    def test_setup_permission(self):
        permission = 'collective.nitf: Setup'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_add_permission(self):
        permission = 'collective.nitf: Add News Article'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_addon_layer(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertIn('INITFLayer', layers)

    def test_link_workflow_changed(self):
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType('Link')
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'one_state_workflow')

    def test_hide_extensions_profiles(self):
        app = self.layer['app']
        request = self.layer['request']
        add_plone_site = AddPloneSite(app, request)
        profiles = add_plone_site.profiles()
        extensions_profiles = profiles['extensions']
        profiles_ids = [profile['id'] for profile in extensions_profiles]
        nitf_profiles = [
            profile_id for profile_id in profiles_ids
            if profile_id.startswith(PROJECTNAME)
        ]
        self.assertEqual([u'collective.nitf:default'], nitf_profiles)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertIn(JS, resource_ids)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertIn(CSS, resource_ids)


class UninstallTest(unittest.TestCase, QIBBB):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.qi = self.uninstall()  # BBB: QI compatibility

    @unittest.skipIf(IS_BBB, 'Plone >= 5.1')
    def test_uninstalled(self):
        self.assertFalse(self.qi.is_product_installed(PROJECTNAME))

    @unittest.skipUnless(IS_BBB, 'Plone < 5.1')
    def test_uninstalled_BBB(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertNotIn('INITFLayer', layers)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertNotIn(JS, resource_ids)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertNotIn(CSS, resource_ids)

    # FIXME: https://github.com/collective/collective.nitf/issues/168
    @unittest.expectedFailure
    def test_link_workflow_restored(self):
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType('Link')
        # default binding
        self.assertEqual(len(chain), 0)
