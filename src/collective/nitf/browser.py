# -*- coding: utf-8 -*-

import math

from Acquisition import aq_inner

from five import grok
from zope.interface import Interface

from Products.ATContentTypes.interfaces import IATImage
from Products.ATContentTypes.interfaces import IATFile
from Products.ATContentTypes.interfaces import IATLink
from Products.CMFPlone.utils import getToolByName

from plone.app.layout.viewlets.interfaces import IAboveContentBody
from plone.app.layout.viewlets.interfaces import IHtmlHeadLinks
from plone.directives import dexterity

from collective.nitf.content import INITF
from collective.nitf.interfaces import INITFBrowserLayer, IMediaView

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

    def update(self):
        self.context = aq_inner(self.context)
        self.catalog = getToolByName(self.context, 'portal_catalog')

    def _get_brains(self, object_provides=None):
        """Return a list of brains inside the NITF object.
        """
        self.update()
        path = '/'.join(self.context.getPhysicalPath())
        brains = self.catalog(object_provides=object_provides,
                              path=path,
                              sort_on='getObjPositionInParent')

        return brains

    def get_images(self):
        """Return a list of image brains inside the NITF object.
        """
        return self._get_brains(IATImage.__identifier__)

    def get_files(self):
        """Return a list of file brains inside the NITF object.
        """
        return self._get_brains(IATFile.__identifier__)

    def get_links(self):
        """Return a list of link brains inside the NITF object.
        """
        return self._get_brains(IATLink.__identifier__)

    def get_media(self):
        """Return a list of object brains inside the NITF object.
        """
        media_interfaces = [IATImage.__identifier__,
                            IATFile.__identifier__,
                            IATLink.__identifier__]

        return self._get_brains(media_interfaces)

    # XXX: is this waking up the object more than once when calling
    # imageCaption() and tag()?
    def getImage(self):
        images = self.get_images()
        if len(images) > 0:
            return images[0].getObject()
        return None

    def imageCaption(self):
        image = self.getImage()
        if image is not None:
            return image.Description()

    def tag(self, **kwargs):
        image = self.getImage()
        if image is not None:
            return image.tag(**kwargs)


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
