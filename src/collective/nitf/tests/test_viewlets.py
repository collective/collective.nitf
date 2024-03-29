# -*- coding: utf-8 -*-
"""Tests of viewlets.

For more information on how to test viewlets, see:
http://docs.plone.org/develop/plone/views/viewlets.html
"""
from collective.nitf.browser import NITFBelowContentTitleContents
from collective.nitf.interfaces import INITFLayer
from collective.nitf.testing import FRACTAL
from collective.nitf.testing import INTEGRATION_TESTING
from collective.nitf.tests.api_hacks import set_file_field
from plone import api
from Products.Five.browser import BrowserView as View
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class DocumentBylineViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, INITFLayer)

        self.manager = "plone.belowcontenttitle"
        self.viewlet = "plone.belowcontenttitle.documentbyline"

        with api.env.adopt_roles(["Manager"]):
            self.n1 = api.content.create(
                self.portal,
                "collective.nitf.content",
                "n1",
            )

    def _get_viewlet_manager(self, context, request=None, name=None):
        self.assertIsNotNone(name)
        if request is None:
            request = self.request
        view = View(context, request)
        manager = getMultiAdapter(
            (context, request, view),
            IViewletManager,
            name,
        )
        return manager

    def _get_viewlet(self, context, manager, name):
        manager = self._get_viewlet_manager(context, name=manager)
        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == name]
        self.assertEqual(len(viewlet), 1)
        return viewlet[0]

    def test_non_overrides(self):
        context = self.portal
        documentbyline = self._get_viewlet(context, self.manager, self.viewlet)
        self.assertFalse(hasattr(documentbyline, "_search_member_by_name"))

    def test_overrides(self):
        context = self.n1
        documentbyline = self._get_viewlet(context, self.manager, self.viewlet)
        self.assertTrue(hasattr(documentbyline, "_search_member_by_name"))

    def test_render_empty_byline(self):
        documentbyline = self._get_viewlet(self.n1, self.manager, self.viewlet)

        self.assertNotIn(
            u'<span class="documentAuthor">',
            documentbyline.render(),
        )

    def test_render_non_existent_user(self):
        documentbyline = self._get_viewlet(self.n1, self.manager, self.viewlet)

        self.n1.byline = u"Keith Moon"
        self.assertIn(
            u'<span class="documentAuthor">',
            documentbyline.render(),
        )
        self.assertNotIn(u'property="rnews:author"', documentbyline.render())
        self.assertIn(u"Keith Moon", documentbyline.render())

    def test_render_existent_user(self):
        api.user.create(
            email="foo@bar.com",
            username="keith-moon",
            properties=dict(fullname=u"Keith Moon"),
        )

        documentbyline = self._get_viewlet(self.n1, self.manager, self.viewlet)

        self.n1.byline = u"Keith Moon"
        self.assertIn(
            u'<span class="documentAuthor">',
            documentbyline.render(),
        )
        self.assertIn(
            u'<a href="http://nohost/plone/author/keith-moon" property="rnews:author">Keith Moon</a>',
            documentbyline.render(),
        )

    def test_render_viewlet_plone_below_contenttitle_file(self):
        file = api.content.create(
            self.n1,
            "File",
            title="foo_related",
            description="bar_related",
        )
        set_file_field(file, FRACTAL, "image/jpeg")
        viewlet = NITFBelowContentTitleContents(
            self.portal,
            self.request,
            None,
            None,
        )
        viewlet.update()
        rendered = viewlet.render()
        self.assertIn("foo_related", rendered)
        self.assertIn("bar_related", rendered)

    def test_empty_render_viewlet_plone_below_contenttitle(self):
        viewlet = NITFBelowContentTitleContents(
            self.portal,
            self.request,
            None,
            None,
        )
        viewlet.update()
        rendered = viewlet.render()
        empty_rendering = u"\n"
        self.assertEqual(empty_rendering, rendered)
