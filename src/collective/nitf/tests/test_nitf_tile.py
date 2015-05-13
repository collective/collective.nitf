# -*- coding: utf-8 -*-
from collective.cover.tests.base import TestTileMixin
from collective.nitf.testing import INTEGRATION_TESTING
from collective.nitf.tiles.nitf import INITFTile
from collective.nitf.tiles.nitf import NITFTile
from mock import Mock
from plone import api

import unittest


class NITFTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(NITFTileTestCase, self).setUp()
        self.tile = NITFTile(self.cover, self.request)
        self.tile.__name__ = u'collective.nitf'
        self.tile.id = u'test'

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = INITFTile
        self.klass = NITFTile
        super(NITFTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['collective.nitf.content'])

    def test_render_empty(self):
        msg = u'Drag&amp;drop a News Article here.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())

    def test_render_title(self):
        kwargs = dict(title=u'foo', subtitle=u'bar', section=u'baz')
        with api.env.adopt_roles(['Manager']):
            n1 = api.content.create(
                self.portal, 'collective.nitf.content', 'n1', **kwargs)

        self.tile.populate_with_object(n1)
        rendered = self.tile()
        self.assertIn(u'foo', rendered)
        self.assertIn(u'bar', rendered)
        self.assertIn(u'baz', rendered)
