# -*- coding: utf-8 -*-
from collective.nitf.config import PROJECTNAME
from collective.nitf.interfaces import INITF
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api
from plone.app.textfield.value import RichTextValue

import unittest


class CatalogTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.catalog = self.portal['portal_catalog']

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(
                self.portal, 'collective.nitf.content', 'n1')
            self.n2 = api.content.create(
                self.portal, 'collective.nitf.content', 'n2')

    def test_interface_indexed(self):
        result = self.catalog(object_provides=INITF.__identifier__)
        self.assertEqual(2, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())
        self.assertEqual(result[1].getURL(), self.n2.absolute_url())

    def test_subtitle_indexed(self):
        self.n1.subtitle = 'subtitle'
        self.n1.reindexObject()
        result = self.catalog(subtitle='subtitle')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_byline_indexed(self):
        self.n1.byline = u'Héctor Velarde'
        self.n1.reindexObject()
        result = self.catalog(byline='Héctor')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_genre_indexed(self):
        self.n1.genre = u'Actuality'
        self.n1.reindexObject()
        result = self.catalog(genre=u'Actuality')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_section_indexed(self):
        self.n1.section = u'foo'
        self.n1.reindexObject()
        result = self.catalog(section=u'foo')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_urgency_indexed(self):
        from collective.nitf.config import HIGH
        self.n1.urgency = HIGH
        self.n1.reindexObject()
        results = self.catalog(urgency=HIGH)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_location_indexed(self):
        self.n1.location = u'México, DF'
        self.n1.reindexObject()
        result = self.catalog(location='México')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_searchable_text_indexed(self):
        """ SearchableText must contain id, title, subtitle, abstract, author,
        body text and location as plain text.
        """
        self.n1.title = u'title'
        self.n1.subtitle = u'subtitle'
        self.n1.description = u'abstract'
        self.n1.byline = u'Héctor Velarde'
        self.n1.text = RichTextValue(u'body text', 'text/plain', 'text/html')
        self.n1.location = u'México, DF'
        self.n1.reindexObject()
        result = self.catalog(SearchableText='n1')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='title')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='subtitle')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='abstract')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='Héctor')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='body')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

        result = self.catalog(SearchableText='México')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())

    def test_searchable_text_missing_fields(self):
        """ Adding an NITF with its title only should be enough to get the
        SearchableText index indexed.
        """
        with api.env.adopt_roles(['Manager']):
            nitf = api.content.create(
                self.portal, 'collective.nitf.content', 'nitf')

        nitf.title = u'title'
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

        nitf.subtitle = u'subtitle'
        nitf.reindexObject()
        result = self.catalog(SearchableText='subtitle')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='abstract')
        self.assertEqual(0, len(result))

        nitf.description = u'abstract'
        nitf.reindexObject()
        result = self.catalog(SearchableText='abstract')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='author')
        self.assertEqual(0, len(result))

        nitf.byline = u'Héctor Velarde'
        nitf.reindexObject()
        result = self.catalog(SearchableText='Héctor')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='body')
        self.assertEqual(0, len(result))

        nitf.text = RichTextValue('body text', 'text/plain', 'text/html')
        nitf.reindexObject()
        result = self.catalog(SearchableText='body')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='México')
        self.assertEqual(0, len(result))

        nitf.location = u'México, DF'
        nitf.reindexObject()
        result = self.catalog(SearchableText='México')
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

        result = self.catalog(SearchableText='Héctor')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='body')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

        result = self.catalog(SearchableText='México')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), nitf.absolute_url())

    def test_catalog_not_lost_on_package_reinstall(self):
        """ Catalog information should not be lost on package reinstall.
        https://github.com/collective/collective.nitf/issues/33
        """
        self.n1.byline = u'Héctor Velarde'
        self.n1.reindexObject()
        qi = self.portal['portal_quickinstaller']
        qi.reinstallProducts(products=[PROJECTNAME])
        result = self.catalog(SearchableText='Héctor')
        self.assertEqual(1, len(result))
        self.assertEqual(result[0].getURL(), self.n1.absolute_url())
