# -*- coding: utf-8 -*-
# BBB: this module will be removed in version 3.0
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implementer

import logging
import warnings


logging.captureWarnings(True)


class ILatestSectionableNITFPortlet(IPortletDataProvider):
    """BBB."""


@implementer(ILatestSectionableNITFPortlet)
class Assignment(base.Assignment):
    """BBB."""


class Renderer(base.Renderer):
    """BBB."""

    def render(self):
        msg = (
            'Use of portlet "Latest Sectionable NITF" is deprecated; '
            'remove assignment manually from {0}'.format(self.context))
        warnings.warn(msg, DeprecationWarning)


class AddForm(base.AddForm):
    """BBB."""


class EditForm(base.EditForm):
    """BBB."""
