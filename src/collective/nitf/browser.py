# -*- coding: utf-8 -*-

import json
import math

from Acquisition import aq_inner

from five import grok
from zope.container.interfaces import INameChooser
from zope.component import queryMultiAdapter
from zope.interface import Interface

from Products.ATContentTypes.interfaces import IATLink
from Products.CMFPlone.utils import getToolByName

from plone.app.layout.viewlets.interfaces import IAboveContentBody
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.directives import dexterity

from collective.nitf.content import INITF
from collective.nitf.interfaces import INITFBrowserLayer, IMediaView

IMAGE_MIMETYPES = ['image/jpeg', 'image/gif', 'image/png']

grok.templatedir('templates')


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
