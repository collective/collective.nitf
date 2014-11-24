# -*- coding: utf-8 -*-
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api

import unittest


class PermissionsTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(
                self.portal, 'collective.nitf.content', 'n1')

    def test_add_permissions(self):
        permission = 'collective.nitf: Add News Article'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)

    # TODO: find a better way to test this
    def test_owner_permissions(self):
        # the owner can add Images, Files and Links
        # Manager is the owner in this context
        permissions = self.n1.permissionsOfRole('Manager')
        permissions = [p['name'] for p in permissions if p['selected']]
        self.assertIn('ATContentTypes: Add Image', permissions)
        self.assertIn('ATContentTypes: Add File', permissions)
        self.assertIn('ATContentTypes: Add Link', permissions)
