# -*- coding: utf-8 -*-

import json
import math
from inspect import ismethod

from Acquisition import aq_inner

from five import grok
from zope.container.interfaces import INameChooser
from zope.component import queryMultiAdapter
from zope.interface import Interface

from Products.Archetypes.utils import shasattr
from Products.ATContentTypes.interfaces import IATLink
from Products.CMFPlone.utils import getToolByName

from plone.app.layout.viewlets.interfaces import IAboveContentBody
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.directives import dexterity

from collective.nitf.content import INITF
from collective.nitf.interfaces import INITFBrowserLayer, IMediaView

IMAGE_MIMETYPES = ['image/jpeg', 'image/gif', 'image/png']

grok.templatedir('templates')


# TODO: enable_form_tabbing must be user selectable
class AddForm(dexterity.AddForm):
    """Default view looks like a News Item.
    """
    grok.name('collective.nitf.content')
    grok.layer(INITFBrowserLayer)

    enable_form_tabbing = False


class EditForm(dexterity.EditForm):
    """Default view looks like a News Item.
    """
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)

    enable_form_tabbing = False


class View(dexterity.DisplayForm):
    """Default view looks like a News Item.
    """
    grok.context(INITF)
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)

    def image(self):
        imgs = self.get_media_files(types=('Image',), limit=1)
        if len(imgs):
            return imgs[0]

    def update(self):
        self.context = aq_inner(self.context)
        self.catalog = getToolByName(self.context, 'portal_catalog')

    def get_media_files(self, types=('Image', 'File',), limit=None):
        context_path = '/'.join(self.context.getPhysicalPath())
        media_brains = self.catalog.searchResults(
                        {'Type': types,
                         'path': {'query': context_path,
                                  'depth': 1},
                         },
                        sort_on="getObjPositionInParent",
                        limit=limit)
        media_items = []
        for brain in media_brains:
            ibrain = {'id': brain.id,
                      'title': brain.Title,
                      'description': brain.Description,
                      'image_url': brain.getURL(),
                      }
            media_items.append(ibrain)
        return media_items

    def images(self):
        self.update()
        return self.get_media_files(types=('Image',))

    def files(self):
        self.update()
        return self.get_media_files(types=('File',))

    def links(self):
        """Return a catalog search result of links to show.
        """
        self.update()

        links = self.catalog(object_provides=IATLink.__identifier__,
                        path='/'.join(self.context.getPhysicalPath()),
                        sort_on='getObjPositionInParent')

        links = [brain.getObject() for brain in links]
        links = [{'title': obj.Title(),
                  'url': obj.remoteUrl,
                  'description': obj.Description()} for obj in links]
        return links


class Display_Macros(View):
    grok.context(INITF)
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)


class Gallery(View):
    grok.context(INITF)
    grok.implements(IMediaView)
    grok.layer(INITFBrowserLayer)
    grok.require('zope2.View')


class Folder_Summary_View(grok.View):
    grok.context(Interface)
    grok.layer(INITFBrowserLayer)
    grok.name("folder_summary_view")
    grok.require('zope2.View')


class MediaViewletManager(grok.ViewletManager):
    grok.context(INITF)
    grok.name('collective.nitf.carousel')
    grok.view(Display_Macros)
    grok.layer(INITFBrowserLayer)


class MediaViewlet(grok.Viewlet):
    grok.context(INITF)
    grok.name('collective.nitf.media.tile')
    grok.viewletmanager(IAboveContentBody)
    grok.view(IMediaView)
    grok.template('media_viewlet')
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)

    image_size = 'tile'

    def update(self, image_size=None):
        if image_size is not None:
            self.image_size = image_size
        self.media_name = "media-%s" % self.image_size

    def mediaRows(self, keys, cols='5'):
        rows = []
        if not cols or not keys:
            return rows
        rows_number = int(math.ceil(float(len(keys)) / float(cols)))
        for row in range(rows_number):
            this_row = []
            start = row * int(cols)
            end = start + int(cols)
            for key in keys[start:end]:
                this_row.append(key)
            rows.append(this_row)
        return rows


class MediaGalleryViewlet(MediaViewlet):
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)
    grok.name('collective.nitf.media.gallery')
    grok.order(0)
    grok.template('gallery_viewlet')
    grok.view(Gallery)
    grok.viewletmanager(IAboveContentBody)

    image_size = 'tile'


class MediaPreviewViewlet(MediaViewlet):
    grok.context(INITF)
    grok.name('collective.nitf.media.preview')
    grok.viewletmanager(MediaViewletManager)
    grok.view(View)
    grok.layer(INITFBrowserLayer)

    image_size = 'preview'


class MediaLinksViewlet(grok.Viewlet):
    grok.context(INITF)
    grok.name('collective.nitf.links.media')
    grok.template('media_links')
    grok.viewletmanager(IHtmlHeadLinks)
    grok.layer(INITFBrowserLayer)


class NITF(dexterity.DisplayForm):
    """Shows news article in NITF XML format.
    """
    grok.context(INITF)
    grok.require('zope2.View')


class Organize(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('cmf.ModifyPortalContent')
