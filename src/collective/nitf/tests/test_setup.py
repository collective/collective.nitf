# -*- coding: utf-8 -*-
from collective.nitf.config import PROJECTNAME
from collective.nitf.testing import HAS_COVER
from collective.nitf.testing import INTEGRATION_TESTING
from collective.nitf.testing import IS_PLONE_5
from plone import api
from plone.browserlayer.utils import registered_layers

import unittest


DEPENDENCIES = (
    'collective.js.cycle2',
    'collective.js.jqueryui',
)

JS = '++resource++collective.nitf/nitf.js'
CSS = '++resource++collective.nitf/nitf.css'


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

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertIn(JS, resource_ids)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertIn(CSS, resource_ids)

    @unittest.skipUnless(HAS_COVER, 'plone.app.tiles must be installed')
    def test_tile(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(u'collective.nitf', tiles)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('INITFLayer', layers)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry_removed(self):
        resource_ids = self.portal.portal_javascripts.getResourceIds()
        self.assertNotIn(JS, resource_ids)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertNotIn(CSS, resource_ids)

    @unittest.skipUnless(HAS_COVER, 'plone.app.tiles must be installed')
    def test_tile_removed(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertNotIn(u'collective.nitf', tiles)

    # FIXME: https://github.com/collective/collective.nitf/issues/168
    @unittest.expectedFailure
    def test_link_workflow_restored(self):
        workflow_tool = self.portal.portal_workflow
        chain = workflow_tool.getChainForPortalType('Link')
        # default binding
        self.assertEqual(len(chain), 0)
