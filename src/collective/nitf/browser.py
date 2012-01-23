# -*- coding: utf-8 -*-

import math
import mimetypes

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

MEDIA = """
<media id="media:%s" media-type="%s">
    <media-metadata id="media-id:%s" name="id" value="urn:uuid:%s" />
    <media-reference mime-type="%s" source="%s" alternate-text="%s"%s%s />
</media>
"""


class NITF(View):
    """Shows news article in NITF XML format.
    """
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)
    grok.name('nitf')
    grok.require('zope2.View')

    def _get_mediatype(self, mimetype):
        """Return one of the possible values of the media-type controlled
        vocabulary.
        """
        # 'data' and 'other' are also part of the controlled vocabulary; we
        # are not going to use 'data'
        vocabulary = ['text', 'audio', 'image', 'video', 'application']
        for i in vocabulary:
            if mimetype.find(i) != -1:
                return i

        return 'other'

    def get_media(self):
        """Return a list of object brains inside the NITF object.
        """
        media = []
        # XXX: we could honor original order calling the get_media() method in
        # View; how can we do that?
        results = self.get_images() + self.get_files()
        for r in results:
            obj = r.getObject()
            id = obj.UID()
            source = obj.absolute_url()
            (mimetype, encoding) = mimetypes.guess_type(source)
            # if no mime type is detected, result is None; we must change it
            mimetype = mimetype and mimetype or ''
            mediatype = self._get_mediatype(mimetype)
            alternate_text = obj.title_or_id()
            # we only include height and/or width if we have a value for them
            height = obj.getHeight()
            height = height and ' height="%s"' % obj.getHeight() or ''
            width = obj.getWidth()
            width = width and ' width="%s"' % obj.getWidth() or ''
            m = MEDIA % (id, mediatype,
                         id, id,
                         mimetype, source, alternate_text, height, width)
            media.append(m)

        return media


class Organize(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('cmf.ModifyPortalContent')
