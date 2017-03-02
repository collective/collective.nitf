# -*- coding: utf-8 -*-
"""BBB: Backwards compatibility code to be removed after release 2.2b1."""
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implementer


class ILatestSectionableNITFPortlet(IPortletDataProvider):
    """BBB."""


@implementer(ILatestSectionableNITFPortlet)
class Assignment(base.Assignment):
    """BBB."""


class Renderer(base.Renderer):
    """BBB."""
    def render(self):
        return u''


class AddForm(base.AddForm):
    """BBB."""


class EditForm(base.EditForm):
    """BBB."""
