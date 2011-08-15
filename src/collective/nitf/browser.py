# -*- coding: utf-8 -*-

import json
import math

from Acquisition import aq_inner

from five import grok
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.interface import Interface

from Products.ATContentTypes.interfaces import IATLink
from Products.CMFPlone.utils import getToolByName

from plone.app.layout.viewlets.interfaces import IAboveContentBody
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.directives import dexterity
from plone.registry.interfaces import IRegistry

from collective.nitf import INITFBrowserLayer
from collective.nitf.content import INITF
from collective.nitf.controlpanel import INITFSettings

VIDEO_MIMETYPES = ['video/mp4', 'video/x-flv']
IMAGE_MIMETYPES = ['image/jpeg', 'image/gif', 'image/png']

grok.templatedir('templates')


class IMediaView(Interface):
    """Marker interface for media views.
    """


class Media_View(dexterity.DisplayForm):
    grok.context(INITF)
    grok.name('media_view')
    grok.title(u'Media View')
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)

    def update(self):
        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.get_images()

    def get_images(self):
        return self.get_media_files(types=('Image',))

    def get_videos(self):
        return self.get_media_files(types=('File',))

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
            if brain.getObject().getContentType() in IMAGE_MIMETYPES:
                ibrain['media_type'] = 'image'
            elif brain.getObject().getContentType() in VIDEO_MIMETYPES:
                ibrain['media_type'] = 'video'
            else:
                ibrain['media_type'] = None
            media_items.append(ibrain)
        return media_items


class NewsItem_View(Media_View):
    grok.context(INITF)
    grok.name('newsitem_view')
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)

    def image(self):
        imgs = self.get_media_files(types=('Image',), limit=1)
        if len(imgs):
            return imgs[0]


class NewsMedia_View(NewsItem_View):
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)
    grok.name('newsmedia_view')
    grok.require('zope2.View')
    grok.template('newsmedia_view')
    grok.view(IMediaView)


class MediaViewletManager(grok.ViewletManager):
    grok.context(INITF)
    grok.name('collective.nitf.carousel')
    grok.view(Media_View)
    grok.layer(INITFBrowserLayer)


class MediaViewlet(grok.Viewlet):
    grok.context(INITF)
    grok.name('collective.nitf.media.tile')
    grok.viewletmanager(IAboveContentBody)
    grok.view(NewsMedia_View)
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


class MediaPreviewViewlet(MediaViewlet):
    grok.context(INITF)
    grok.name('collective.nitf.media.preview')
    grok.viewletmanager(MediaViewletManager)
    grok.view(Media_View)
    grok.layer(INITFBrowserLayer)

    image_size = 'preview'


class MediaLinksViewlet(grok.Viewlet):
    grok.context(INITF)
    grok.name('collective.nitf.links.media')
    grok.template('media_links')
    grok.viewletmanager(IHtmlHeadLinks)
    grok.layer(INITFBrowserLayer)


class Embed(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('zope2.View')

    def links(self):
        """Return a catalog search result of links to show.
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        links = catalog(object_provides=IATLink.__identifier__,
                        path='/'.join(context.getPhysicalPath()),
                        sort_on='getObjPositionInParent')

        links = [brain.getObject() for brain in links]
        links = [{'title': obj.Title(),
                  'url': obj.remoteUrl,
                  'description': obj.Description()} for obj in links]
        return links

    def key(self):
        """Return Embedly key.
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(INITFSettings)
        return settings.embedly_key


class Media_Sorter(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('cmf.ModifyPortalContent')


class Media_Uploader(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('cmf.ModifyPortalContent')

    files = []

    def __call__(self, *args, **kwargs):
        if hasattr(self.request, "REQUEST_METHOD"):
            if self.request["REQUEST_METHOD"] == "POST":
                if getattr(self.request, "files[]", None) is not None:
                    files = self.request['files[]']

                    json_view = queryMultiAdapter((self.context, self.request), name=u"api")
                    if json_view:
                        return json_view()
        return super(Media_Uploader, self).__call__(*args, **kwargs)


class JSON_View(grok.View):
    grok.context(INITF)
    grok.name('api')
    grok.require('cmf.ModifyPortalContent')

    json_var = {'name': 'File-Name.jpg',
                'size': 999999,
                'url': '\/\/nohost.org',
                'thumbnail_url': '//nohost.org',
                'delete_url': '//nohost.org',
                'delete_type': '//nohost.org',
                }

    def __call__(self, json_var=None):
        self.response.setHeader('Content-Type', 'text/plain')
        if isinstance(json_var, basestring):
            self.json_var = json_var
        return super(JSON_View, self).__call__()

    def uploads(self):
        """ """
        pass

    def render(self):
        if getattr(self.request, "REQUEST_METHOD", None) is not None:
            self.files = self.request["REQUEST_METHOD"]
            return json.dumps(self.json_var)
