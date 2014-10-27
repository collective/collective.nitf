# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from DateTime import DateTime
from plone import api
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling
from plone.app.layout.viewlets.content import DocumentBylineViewlet
from plone.dexterity.browser.view import DefaultView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import json
import pkg_resources

PLONE_VERSION = pkg_resources.require('Plone')[0].version


class View(DefaultView):

    """Default view looks like a News Item."""

    def update(self):
        self.context = aq_inner(self.context)

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

    def has_images(self):
        """Return the number of images inside the NITF object."""
        return len(self.get_images())

    def get_files(self):
        """Return a list of file brains inside the NITF object."""
        return self._get_brains('File')

    def has_files(self):
        """Return the number of files inside the NITF object."""
        return len(self.get_files())

    def get_links(self):
        """Return a list of link brains inside the NITF object."""
        return self._get_brains('Link')

    def has_links(self):
        """Return the number of links inside the NITF object."""
        return len(self.get_links())

    def get_media(self):
        """Return a list of object brains inside the NITF object."""
        media_ct = [x.title for x in self.context.allowedContentTypes()]
        return self._get_brains(media_ct)

    def has_media(self):
        """Return the number of media inside the NITF object."""
        return len(self.get_media())


class NitfGalleria(DefaultView):

    def imagesJson(self):
        """ """
        try:
            img_brains = self.get_images()
        except IndexError:
            img_brains = None
        if img_brains:
            data = [{'image': str(brain.getPath() + '/image_preview'),
                     'title': brain.Title,
                     'description': brain.Description, 'right': brain.Rights(),
                     'link': brain.getURL()} for brain in img_brains]
        else:
            data = []

        return json.dumps(data)


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

    index = ViewPageTemplateFile("templates/nitf_byline.pt")

    def getMemberInfoByName(self, fullname):
        membership = api.portal.get_tool('portal_membership')
        members = membership.searchForMembers(name=fullname)
        if members:
            member = members[0].getUserId()  # we care only about the first
            return membership.getMemberInfo(member)

    def byline(self):
        member = self.getMemberInfoByName(self.context.byline)
        if member:
            return member['username']

    def author(self):
        return self.getMemberInfoByName(self.context.byline)

    def authorname(self):
        return self.context.byline

    def pub_date(self):
        """Return object effective date.

        Return None if publication date is switched off in global site settings
        or if Effective Date is not set on object.
        """
        if PLONE_VERSION >= '4.3':
            return super(NITFBylineViewlet, self).pub_date()  # use parent's method

        # compatibility for Plone < 4.3
        # check if we are allowed to display publication date
        properties = api.portal.get_tool('portal_properties')
        site_properties = getattr(properties, 'site_properties')
        if not site_properties.getProperty('displayPublicationDateInByline'):
            return None

        # check if we have Effective Date set
        date = self.context.EffectiveDate()
        if not date or date == 'None':
            return None

        return DateTime(date)
