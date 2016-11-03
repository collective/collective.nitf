# -*- coding: utf-8 -*-
from collective.nitf import config as c
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api

import unittest


class CollectionTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.folder = api.content.create(
                self.portal, 'Folder', 'test')
            self.c1 = api.content.create(
                self.portal, 'Collection', 'c1')

        self.c1.setQuery([
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ['collective.nitf.content']
            }
        ])

    def test_urgency_filter(self, ):
        self.assertEqual(len(self.c1.queryCatalog()), 0)

        n1 = api.content.create(self.folder, 'collective.nitf.content', 'n1')
        n1.urgency = c.LOW
        n1.reindexObject()
        self.assertEqual(len(self.c1.queryCatalog()), 1)

        n2 = api.content.create(self.folder, 'collective.nitf.content', 'n2')
        n2.urgency = c.NORMAL
        n2.reindexObject()
        self.assertEqual(len(self.c1.queryCatalog()), 2)

        n3 = api.content.create(self.folder, 'collective.nitf.content', 'n3')
        n3.urgency = c.HIGH
        n3.reindexObject()
        self.assertEqual(len(self.c1.queryCatalog()), 3)

        self.c1.setQuery([
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ['collective.nitf.content']
            },
            {
                'i': 'urgency',
                'o': 'plone.app.querystring.operation.intselection.is',
                'v': [c.LOW]
            }
        ])
        self.assertEqual(len(self.c1.queryCatalog()), 1)
        expected = self.c1.queryCatalog()[0].getObject()
        self.assertEqual(n1, expected)

        self.c1.setQuery([
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ['collective.nitf.content']
            },
            {
                'i': 'urgency',
                'o': 'plone.app.querystring.operation.intselection.is',
                'v': [c.NORMAL]
            }
        ])
        self.assertEqual(len(self.c1.queryCatalog()), 1)
        expected = self.c1.queryCatalog()[0].getObject()
        self.assertEqual(n2, expected)

        self.c1.setQuery([
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ['collective.nitf.content']
            },
            {
                'i': 'urgency',
                'o': 'plone.app.querystring.operation.intselection.is',
                'v': [c.HIGH]
            }
        ])
        self.assertEqual(len(self.c1.queryCatalog()), 1)
        expected = self.c1.queryCatalog()[0].getObject()
        self.assertEqual(n3, expected)

        self.c1.setQuery([
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ['collective.nitf.content']
            },
            {
                'i': 'urgency',
                'o': 'plone.app.querystring.operation.intselection.is',
                'v': [c.NORMAL, c.HIGH]
            }
        ])
        self.assertEqual(len(self.c1.queryCatalog()), 2)
        expected = [b.getObject() for b in self.c1.queryCatalog()]
        self.assertEqual([n2, n3], expected)

    def test_render_view_methods(self, ):
        # https://github.com/collective/collective.nitf/issues/178
        from collective.nitf.testing import get_image
        from collective.nitf.testing import IMAGES
        from collective.nitf.tests.api_hacks import set_image_field

        # news article with lead image
        obj = api.content.create(self.folder, 'collective.nitf.content', 'n1')
        api.content.create(obj, 'Image', 'img1')
        set_image_field(obj['img1'], get_image(IMAGES[0]), 'image/jpeg')
        # news article without lead image
        api.content.create(self.folder, 'collective.nitf.content', 'n2')
        assert len(self.c1.queryCatalog()) == 2

        # traverse view methods and assert they are rendered without errors
        types = self.portal['portal_types']
        view_methods = types['Collection'].view_methods
        for view in view_methods:
            rendered = self.c1.restrictedTraverse(view)()
            self.assertIsInstance(rendered, unicode)
