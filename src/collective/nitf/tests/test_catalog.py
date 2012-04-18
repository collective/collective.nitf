# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.app.textfield.value import RichTextValue

from collective.nitf.config import PROJECTNAME
from collective.nitf.content import INITF
from collective.nitf.testing import INTEGRATION_TESTING


class CatalogTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.catalog = self.portal['portal_catalog']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('collective.nitf.content', 'n1')
        self.folder.invokeFactory('collective.nitf.content', 'n2')
        self.n1 = self.folder['n1']
        self.n2 = self.folder['n2']

    def test_interface_indexed(self):
        result = self.catalog(object_provides=INITF.__identifier__)
        self.assertEqual(2, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())
        self.assertEqual(result[1].getURL(), self.n2.absolute_url())

    def test_subtitle_indexed(self):
        self.n1.subtitle = 'The subtitle'
        self.n1.reindexObject()
        result = self.catalog(subtitle='The subtitle')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_byline_indexed(self):
        self.n1.byline = 'Author'
        self.n1.reindexObject()
        result = self.catalog(byline='Author')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_genre_indexed(self):
        self.n1.genre = 'News Type'
        self.n1.reindexObject()
        result = self.catalog(genre='News Type')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_section_indexed(self):
        self.n1.section = 'Section'
        self.n1.reindexObject()
        result = self.catalog(section='Section')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_urgency_indexed(self):
        self.n1.urgency = '5'
        self.n1.reindexObject()
        result = self.catalog(urgency='5')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_location_indexed(self):
        self.n1.location = 'Mexico City'
        self.n1.reindexObject()
        result = self.catalog(location='Mexico City')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_searchable_text_indexed(self):
        """ SearchableText must contain id, title, subtitle, abstract, author,
        body text and location as plain text.
        """
        self.n1.title = 'The title'
        self.n1.subtitle = 'The subtitle'
        self.n1.description = 'Abstract'
        self.n1.byline = 'Author'
        self.n1.text = RichTextValue('Body text', 'text/plain', 'text/html')
        self.n1.location = 'Mexico City'
        self.n1.reindexObject()
        result = self.catalog(SearchableText='n1')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='The title')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='The subtitle')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='Abstract')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='Author')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='Body text')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='Mexico City')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_searchable_text_missing_fields(self):
        """ Adding an NITF with its title only should be enough to get the
        SearchableText index indexed.
        """
        self.folder.invokeFactory('collective.nitf.content', 'nitf')
        nitf = self.folder['nitf']
        nitf.title = 'title'
        nitf.reindexObject()
        result = self.catalog(SearchableText='nitf')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())
        result = self.catalog(SearchableText='title')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        # Now let's start adding the remaining fields one by one, first
        # testing that no results are found, and then they are
        result = self.catalog(SearchableText='subtitle')
        self.assertEqual(0, len(result))

        nitf.subtitle = 'subtitle'
        nitf.reindexObject()
        result = self.catalog(SearchableText='subtitle')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='abstract')
        self.assertEqual(0, len(result))

        nitf.description = 'abstract'
        nitf.reindexObject()
        result = self.catalog(SearchableText='abstract')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='author')
        self.assertEqual(0, len(result))

        nitf.byline = 'author'
        nitf.reindexObject()
        result = self.catalog(SearchableText='author')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='text')
        self.assertEqual(0, len(result))

        nitf.text = RichTextValue('Body text', 'text/plain', 'text/html')
        nitf.reindexObject()
        result = self.catalog(SearchableText='text')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='Mexico City')
        self.assertEqual(0, len(result))

        nitf.location = 'Mexico City'
        nitf.reindexObject()
        result = self.catalog(SearchableText='Mexico City')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        # Finally, let's do some searches to make sure nothing was
        # "de-categorized"
        result = self.catalog(SearchableText='nitf')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='title')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='subtitle')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='abstract')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='author')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='text')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='Mexico City')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

    def test_catalog_not_lost_on_package_reinstall(self):
        """ Catalog information should not be lost on package reinstall.

        Reported in https://github.com/collective/collective.nitf/issues/33

        See http://maurits.vanrees.org/weblog/archive/2009/12/catalog to find
        out how to fix it.
        """
        self.n1.byline = 'author'
        self.n1.reindexObject()
        qi = self.portal['portal_quickinstaller']
        qi.reinstallProducts(products=[PROJECTNAME])
        result = self.catalog(SearchableText='author')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())
