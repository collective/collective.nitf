# -*- coding: utf-8 -*-
from collective.nitf.config import PROJECTNAME
from collective.nitf.interfaces import INITF
from collective.nitf.testing import INTEGRATION_TESTING
from plone import api
from plone.app.textfield.value import RichTextValue

import unittest


class IndexingTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(
                self.portal, 'collective.nitf.content', 'n1')
            self.n2 = api.content.create(
                self.portal, 'collective.nitf.content', 'n2')

    def test_interface_indexed(self):
        results = api.content.find(object_provides=INITF.__identifier__)
        self.assertEqual(2, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())
        self.assertEqual(results[1].getURL(), self.n2.absolute_url())

    def test_portal_type_indexed(self):
        results = api.content.find(portal_type='collective.nitf.content')
        self.assertEqual(2, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())
        self.assertEqual(results[1].getURL(), self.n2.absolute_url())

    def test_id_indexed(self):
        results = api.content.find(id=u'n1')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_title_indexed(self):
        self.n1.title = u'título'
        self.n1.reindexObject()
        results = api.content.find(Title=u'título')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_subtitle_indexed(self):
        self.n1.subtitle = u'subtítulo'
        self.n1.reindexObject()
        results = api.content.find(subtitle=u'subtítulo')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_description_indexed(self):
        self.n1.description = u'descripción'
        self.n1.reindexObject()
        results = api.content.find(Description=u'descripción')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_byline_indexed(self):
        self.n1.byline = u'Héctor Velarde'
        self.n1.reindexObject()
        results = api.content.find(byline='Héctor')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_genre_indexed(self):
        self.n1.genre = u'Actuality'
        self.n1.reindexObject()
        results = api.content.find(genre=u'Actuality')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_section_indexed(self):
        self.n1.section = u'foo'
        self.n1.reindexObject()
        results = api.content.find(section=u'foo')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_urgency_indexed(self):
        from collective.nitf.config import HIGH
        self.n1.urgency = HIGH
        self.n1.reindexObject()
        results = api.content.find(urgency=HIGH)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_location_indexed(self):
        self.n1.location = u'México, DF'
        self.n1.reindexObject()
        results = api.content.find(location='México')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_keywords_indexed(self):
        self.n1.subject = ('foo', 'baz')
        self.n1.reindexObject()
        self.n2.subject = ('bar', 'baz')
        self.n2.reindexObject()
        results = api.content.find(Subject=('foo'))
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())
        results = api.content.find(Subject=('bar'))
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n2.absolute_url())
        results = api.content.find(Subject=('baz'))
        self.assertEqual(2, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())
        self.assertEqual(results[1].getURL(), self.n2.absolute_url())

    def test_id_in_searchable_text(self):
        results = api.content.find(SearchableText='n1')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_title_in_searchable_text(self):
        self.n1.title = u'título'
        self.n1.reindexObject()
        results = api.content.find(SearchableText=u'título')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_subtitle_in_searchable_text(self):
        self.n1.subtitle = u'subtítulo'
        self.n1.reindexObject()
        results = api.content.find(SearchableText=u'subtítulo')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_description_in_searchable_text(self):
        self.n1.description = u'descripción'
        self.n1.reindexObject()
        results = api.content.find(SearchableText=u'descripción')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_byline_in_searchable_text(self):
        self.n1.byline = u'Héctor Velarde'
        self.n1.reindexObject()
        results = api.content.find(SearchableText=u'Héctor')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_text_in_searchable_text(self):
        self.n1.text = RichTextValue(u'texto rico', 'text/plain', 'text/html')
        self.n1.reindexObject()
        results = api.content.find(SearchableText=u'texto rico')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_location_in_searchable_text(self):
        self.n1.location = u'México, DF'
        self.n1.reindexObject()
        results = api.content.find(SearchableText=u'México')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_keywords_in_searchable_text(self):
        self.n1.subject = ('foo', 'baz')
        self.n1.reindexObject()
        self.n2.subject = ('bar', 'baz')
        self.n2.reindexObject()
        results = api.content.find(SearchableText=('foo'))
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())
        results = api.content.find(SearchableText=('bar'))
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n2.absolute_url())
        results = api.content.find(SearchableText=('baz'))
        self.assertEqual(2, len(results))
        results = [r.getURL() for r in results]
        self.assertIn(self.n1.absolute_url(), results)
        self.assertIn(self.n2.absolute_url(), results)

    def test_catalog_not_lost_on_package_reinstall(self):
        """ Catalog information should not be lost on package reinstall.
        https://github.com/collective/collective.nitf/issues/33
        """
        self.n1.byline = u'Héctor Velarde'
        self.n1.reindexObject()
        qi = self.portal['portal_quickinstaller']
        qi.reinstallProducts(products=[PROJECTNAME])
        results = api.content.find(SearchableText='Héctor')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.n1.absolute_url())

    def test_searchable_text_not_in_metadata(self):
        """Confirms that SearchableText is not in metadata."""
        portal_catalog = api.portal.get_tool('portal_catalog')
        self.assertNotIn('SearchableText', portal_catalog.schema())
