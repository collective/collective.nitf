# -*- coding: utf-8 -*-

from collective.nitf import config as c
from collective.nitf.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest2 as unittest


class CollectionTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder.invokeFactory('Collection', 'c1')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.c1 = self.folder['c1']
        self.c1.setQuery([
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ['collective.nitf.content']
            }
        ])

    def test_urgency_filter(self, ):
        self.assertEqual(len(self.c1.queryCatalog()), 0)

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.n1 = self.folder['n1']
        self.n1.urgency = c.LOW
        self.n1.reindexObject()
        self.assertEqual(len(self.c1.queryCatalog()), 1)

        self.folder.invokeFactory('collective.nitf.content', 'n2')
        self.n2 = self.folder['n2']
        self.n2.urgency = c.NORMAL
        self.n2.reindexObject()
        self.assertEqual(len(self.c1.queryCatalog()), 2)

        self.folder.invokeFactory('collective.nitf.content', 'n3')
        self.n3 = self.folder['n3']
        self.n3.urgency = c.HIGH
        self.n3.reindexObject()
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
        expected = self.c1.queryCatalog()[0].getObject()
        self.assertEqual(self.n1, expected)

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
        expected = self.c1.queryCatalog()[0].getObject()
        self.assertEqual(self.n2, expected)

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
        expected = self.c1.queryCatalog()[0].getObject()
        self.assertEqual(self.n3, expected)

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
        expected = [b.getObject() for b in self.c1.queryCatalog()]
        self.assertEqual([self.n2, self.n3], expected)
