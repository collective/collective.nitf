# -*- coding: utf-8 -*-
"""Tests in this module are executed only if collective.cover is installed."""
from collective.nitf.testing import HAS_COVER
from collective.nitf.testing import INTEGRATION_TESTING
from lxml import etree
from mock import Mock
from plone import api

import unittest


if HAS_COVER:
    from collective.cover.tests.base import TestTileMixin
    from collective.nitf.tiles.nitf import INITFTile
    from collective.nitf.tiles.nitf import NITFTile
else:
    class TestTileMixin:
        pass

    def test_suite():
        return unittest.TestSuite()


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

    def test_render(self):
        kwargs = dict(title=u'foo', subtitle=u'bar', section=u'baz')
        with api.env.adopt_roles(['Manager']):
            n1 = api.content.create(
                self.portal, 'collective.nitf.content', 'n1', **kwargs)

        self.tile.populate_with_object(n1)
        html = etree.HTML(self.tile())
        self.assertIn('foo', html.xpath('//h2/a/text()'))
        self.assertIn('bar', html.xpath('//p/text()'))
        self.assertIn('baz', html.xpath('//p/text()'))
        self.assertTrue(html.xpath('//time'))

    def test_alt_atribute_present_in_image(self):
        # https://github.com/collective/collective.nitf/issues/152
        from collective.nitf.testing import FRACTAL
        from collective.nitf.tests.api_hacks import set_image_field

        with api.env.adopt_roles(['Manager']):
            n1 = api.content.create(
                self.portal, 'collective.nitf.content', title='Lorem ipsum')

        image = api.content.create(n1, 'Image', title='Neque porro')
        set_image_field(image, FRACTAL, 'image/jpeg')

        self.tile.populate_with_object(n1)
        html = etree.HTML(self.tile())
        # title of the news article is used as alt attribute
        self.assertIn('Lorem ipsum', html.xpath('//img/@alt'))

    def test_render_deleted_object(self):
        # https://github.com/collective/collective.nitf/issues/154
        with api.env.adopt_roles(['Manager']):
            n1 = api.content.create(
                self.portal, 'collective.nitf.content', title='Lorem ipsum')

        self.tile.populate_with_object(n1)
        api.content.delete(n1)
        # tile's data is cached; reinstantiate it
        self.tile = self.cover.restrictedTraverse('@@collective.nitf/test')
        html = etree.HTML(self.tile())
        # some metadata is still present
        self.assertIn('Lorem ipsum', html.xpath('//h2/a/text()'))
        self.assertFalse(html.xpath('//time'))  # date is ignored
