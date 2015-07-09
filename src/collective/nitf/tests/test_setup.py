# -*- coding: utf-8 -*-
from collective.nitf.config import PROJECTNAME
from collective.nitf.testing import FUNCTIONAL_TESTING
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from plone.testing.z2 import Browser

import unittest

DEPENDENCIES = [
    # 'collective.js.charcount',
    'collective.js.cycle2',
    'collective.js.jqueryui',
]

JS = [
    '++resource++collective.nitf/nitf.js',
]

CSS = [
    '++resource++collective.nitf/styles.css',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

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
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('INITFLayer', layers)

    def test_link_workflow_changed(self):
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType('Link')
        self.assertEqual(len(chain), 1)
        self.assertEqual(chain[0], 'one_state_workflow')

    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for id in JS:
            self.assertIn(id, resource_ids, '{0} not installed'.format(id))

    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertIn(id, resource_ids, '{0} not installed'.format(id))

    def test_tile(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(u'collective.nitf', tiles)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('INITFLayer', layers)

    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        for id in JS:
            self.assertNotIn(id, resource_ids, '{0} not removed'.format(id))

    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        for id in CSS:
            self.assertNotIn(id, resource_ids, '{0} not removed'.format(id))

    def test_tile_removed(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertNotIn(u'collective.nitf', tiles)

    def test_link_workflow_restored(self):
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType('Link')
        # default binding
        self.assertEqual(len(chain), 0)


class StaticResourceTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def test_static_resource(self):
        """We don't use grok to register automatically the static resources anymore
           should be registered via zcml.
        """
        portal = self.layer['portal']
        app = self.layer['app']

        browser = Browser(app)
        portal_url = portal.absolute_url()

        browser.open('%s/++resource++collective.nitf' % portal_url)
        self.assertEqual(browser.headers['status'], '200 Ok')
