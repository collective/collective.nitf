# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets.content import ContentRelatedItems
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.memoize import ram
from Products.Five import BrowserView
from time import time


class View(BrowserView):

    """Default view of a News Article."""

    def _get_brains(self, object_name=None):
        """Return a list of brains inside the NITF object."""
        catalog = api.portal.get_tool("portal_catalog")
        path = "/".join(self.context.getPhysicalPath())
        brains = catalog(Type=object_name, path=path, sort_on="getObjPositionInParent")

        return brains

    def get_images(self):
        """Return a list of image brains inside the NITF object."""
        return self._get_brains("Image")

    def get_files(self):
        """Return a list of file brains inside the NITF object."""
        return self._get_brains("File")


class Slideshow(BrowserView):

    """Slideshow view of a News Article."""


class TextOnly(BrowserView):

    """Text only view of a News Article."""


class NITFBylineViewlet(DocumentBylineViewlet):

    """Override the document byline viewlet to include semantic markup."""

    def _search_member_by_name(self, fullname):
        """Search a user by its full name and return its member
        information.

        :param fullname: full name of the user we are looking for
        :type fullname: unicode
        :returns: member information
        :rtype: dict
        """
        if not fullname:
            return None

        membership = api.portal.get_tool("portal_membership")
        members = membership.searchForMembers(name=fullname)
        if members:
            # in case there are more than one members with the
            # same fullname, we use the first one listed
            member = members[0].getUserId()
            return membership.getMemberInfo(member)

    @ram.cache(lambda method, self, fullname: (time() // 60, fullname))
    def search_member_by_name(self, fullname):
        """Cached version of _search_member_by_name. Caching is done
        for one minute to avoid performance issues when having many
        users on sites using LDAP authentication.
        """
        return self._search_member_by_name(fullname)

    @property
    def author_id(self):
        member = self.search_member_by_name(self.context.byline)
        if member:
            return member["username"]

    def author(self):
        return self.search_member_by_name(self.context.byline)

    def authorname(self):
        return self.context.byline


class NITFBelowContentTitleContents(ContentRelatedItems):
    def related_items(self):
        catalog = api.portal.get_tool("portal_catalog")
        path = "/".join(self.context.getPhysicalPath())
        brains = catalog(
            Type=["Link", "File"],
            path=path,
            sort_on="getObjPositionInParent",
        )
        return brains
