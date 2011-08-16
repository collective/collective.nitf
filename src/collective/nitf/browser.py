# -*- coding: utf-8 -*-
import json
import math
import urllib

from Acquisition import aq_inner
from Acquisition import aq_parent

from five import grok
from zope.container.interfaces import INameChooser
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
            json_view = queryMultiAdapter((self.context, self.request),
                                          name=u"api")
            if self.request["REQUEST_METHOD"] == "POST":
                if getattr(self.request, "files[]", None) is not None:
                    files = self.request['files[]']
                    uploaded = self.upload([files])
                    if uploaded and json_view:
                        upped = []
                        for item in uploaded:
                            upped.append(json_view.getContextInfo(item))
                        return json_view.dumps(upped)
                return json_view()
        return super(Media_Uploader, self).__call__(*args, **kwargs)

    def upload(self, files):
        loaded = []
        namechooser = INameChooser(self.context)
        if not isinstance(files, list):
            files = [files]
        for item in files:
            if item.filename:
                content_type = item.headers.get('Content-Type')
                id_name = namechooser.chooseName(item.filename, self.context)
                portal_type = 'File'
                if content_type in IMAGE_MIMETYPES:
                    portal_type = 'Image'
                try:
                    self.context.invokeFactory(portal_type, id=id_name, file=item)
                    self.context[id_name].reindexObject()
                    newfile = self.context[id_name]
                    loaded.append(newfile)
                except:
                    pass
            if loaded:
                return loaded
            return False


class JSON_View(grok.View):
    grok.context(INITF)
    grok.name('api')
    grok.require('cmf.ModifyPortalContent')

    json_var = {'name': 'File-Name.jpg',
                'size': 999999,
                'url': '\/\/nohost.org',
                'thumbnail_url': '//nohost.org',
                'delete_url': '//nohost.org',
                'delete_type': 'DELETE',
                }

    def __call__(self):
        self.response.setHeader('Content-Type', 'text/plain')
        return super(JSON_View, self).__call__()

    def dumps(self, json_var=None):
        """ """
        if json_var is None:
            json_var = {}
        return json.dumps(json_var)

    def getContextInfo(self, context=None):
        if context is None:
            context = self.context
        context = aq_inner(context)
        container = aq_parent(context)

        context_state = queryMultiAdapter((context, self.request),
                                        name=u'plone_context_state')
        context_name = context_state.object_title()
        context_url = context_state.object_url()
        del_url = context_url
        info = {'name': context_name,
                'url':  context_url,
                'size': context.size(),
                'delete_url':  del_url,
                'delete_type': 'DELETE',
                }
        if context.Type() == 'Image':
            info['thumbnail_url'] = context_url + '/image_thumb'
        return info

    def getContainerInfo(self):
        contents = []
        for item in self.context.objectIds():
            item_info = self.getContextInfo(self.context[item])
            contents.append(item_info)
        return contents

    def render(self):
        return self.dumps(self.getContainerInfo())
