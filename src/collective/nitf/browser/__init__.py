# -*- coding: utf-8 -*-
from plone import api
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.dexterity.browser.view import DefaultView
from plone.memoize import view


class View(DefaultView):

    """Default view of a News Article."""

    def _get_brains(self, object_name=None):
        """Return a list of brains inside the NITF object."""
        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(Type=object_name, path=path,
                         sort_on='getObjPositionInParent')

        return brains

    def get_images(self):
        """Return a list of image brains inside the NITF object."""
        return self._get_brains('Image')

    def get_files(self):
        """Return a list of file brains inside the NITF object."""
        return self._get_brains('File')

    def get_links(self):
        """Return a list of link brains inside the NITF object."""
        return self._get_brains('Link')

    def get_media(self):
        """Return a list of object brains inside the NITF object."""
        media_ct = [x.title for x in self.context.allowedContentTypes()]
        return self._get_brains(media_ct)


class Slideshow(DefaultView):

    """Slideshow view of a News Article."""


class TextOnly(DefaultView):

    """Text only view of a News Article."""


class ImageScaling(BaseImageScaling):

    """View used for generating (and storing) image scales."""

    def __init__(self, context, request):
        self.image = context.getImage()
        self.context = self.image or context
        self.request = request

    def scale(self, fieldname=None, scale=None, height=None, width=None,
              **parameters):
        if not self.image:
            return None
        view = self.image.restrictedTraverse('@@images')
        return view.scale(fieldname, scale, height, width, **parameters)


class NITFBylineViewlet(DocumentBylineViewlet):

    """Override the document byline viewlet to include semantic markup."""

    @view.memoize
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

        membership = api.portal.get_tool('portal_membership')
        members = membership.searchForMembers(name=fullname)
        if members:
            # in case there are more than one members with the
            # same fullname, we use the first one listed
            member = members[0].getUserId()
            return membership.getMemberInfo(member)

    @property
    def author_id(self):
        member = self._search_member_by_name(self.context.byline)
        if member:
            return member['username']

    def author(self):
        return self._search_member_by_name(self.context.byline)

    def authorname(self):
        return self.context.byline
