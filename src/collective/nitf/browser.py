# -*- coding: utf-8 -*-

import mimetypes

from Acquisition import aq_inner

from five import grok
from zope.interface import Interface

from Products.ATContentTypes.interfaces import IATImage
from Products.ATContentTypes.interfaces import IATFile
from Products.ATContentTypes.interfaces import IATLink
from Products.CMFPlone.utils import getToolByName

from plone.directives import dexterity
from plone.uuid.interfaces import IUUID

from collective.nitf.content import INITF
from collective.nitf.interfaces import INITFBrowserLayer

grok.templatedir('templates')


# TODO: enable_form_tabbing must be user selectable
class AddForm(dexterity.AddForm):
    """ Default view looks like a News Item.
    """
    grok.name('collective.nitf.content')
    grok.layer(INITFBrowserLayer)

    enable_form_tabbing = False


class EditForm(dexterity.EditForm):
    """ Default view looks like a News Item.
    """
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)

    enable_form_tabbing = False


class View(dexterity.DisplayForm):
    """ Default view looks like a News Item.
    """
    grok.context(INITF)
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)

    def update(self):
        self.context = aq_inner(self.context)

    def _get_brains(self, object_provides=None):
        """ Return a list of brains inside the NITF object.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(object_provides=object_provides, path=path,
                         sort_on='getObjPositionInParent')

        return brains

    def get_images(self):
        """ Return a list of image brains inside the NITF object.
        """
        return self._get_brains(IATImage.__identifier__)

    def has_images(self):
        """ Return the number of images inside the NITF object.
        """
        return len(self.get_images())

    def get_files(self):
        """ Return a list of file brains inside the NITF object.
        """
        return self._get_brains(IATFile.__identifier__)

    def has_files(self):
        """ Return the number of files inside the NITF object.
        """
        return len(self.get_files())

    def get_links(self):
        """ Return a list of link brains inside the NITF object.
        """
        return self._get_brains(IATLink.__identifier__)

    def has_links(self):
        """ Return the number of links inside the NITF object.
        """
        return len(self.get_links())

    def get_media(self):
        """ Return a list of object brains inside the NITF object.
        """
        media_interfaces = [IATImage.__identifier__,
                            IATFile.__identifier__,
                            IATLink.__identifier__]

        return self._get_brains(media_interfaces)

    def has_media(self):
        """ Return the number of media inside the NITF object.
        """
        return len(self.get_media())

    # The purpose of these methods is to emulate those on News Item
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
        # tag original implementation returns object title in both, alt and
        # title attributes
        image = self.getImage()
        if image is not None:
            return image.tag(**kwargs)

    # These methods are used in scrollable gallery for creating batches
    def _chunks(self, l, n):
        """ Yield successive n-sized chunks from l.
        """
        for i in xrange(0, len(l), n):
            yield l[i:i + n]

    TAG = '<img src="%s/image_%s" alt="%s" title="%s" />'

    def get_images_in_groups(self, n=5, size='thumb'):
        """ Return a list containing groups of n image tags.
        """
        # TODO: check for a valid size
        images = [i.getObject() for i in self.get_images()]
        images = [self.TAG % (i.absolute_url(), size,
                              i.Title(),
                              i.Description()) for i in images]

        return self._chunks(images, n)


# TODO: get rid of this class
class Display_Macros(View):
    grok.context(INITF)
    grok.require('zope2.View')
    grok.layer(INITFBrowserLayer)


class Scrollable(View):
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)
    grok.require('zope2.View')


class Folder_Summary_View(grok.View):
    grok.context(Interface)
    grok.layer(INITFBrowserLayer)
    grok.name("folder_summary_view")
    grok.require('zope2.View')


class NITF(View):
    """ Shows news article in NITF XML format.
    """
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)
    grok.name('nitf')
    grok.require('zope2.View')

    def update(self):
        self.context = aq_inner(self.context)
        self.uuid = IUUID(self.context)

    def _get_mediatype(self, mimetype):
        """ Return one of the possible values of the media-type controlled
        vocabulary.
        """
        # 'data' and 'other' are also part of the controlled vocabulary; we
        # are not going to use 'data'
        vocabulary = ['text', 'audio', 'image', 'video', 'application']
        for i in vocabulary:
            if mimetype.find(i) != -1:
                return i

        return 'other'

    MEDIA = """
<media media-type="%s">
    <media-reference mime-type="%s" source="%s" alternate-text="%s"%s%s />
    <media-caption>%s</media-caption>
</media>"""

    def get_media(self):
        """ Return a list of object brains inside the NITF object.
        """
        media = []
        # XXX: we could honor original order calling the get_media() method in
        # View; how can we do that?
        results = self.get_images() + self.get_files()
        for r in results:
            obj = r.getObject()
            source = obj.absolute_url()
            (mimetype, encoding) = mimetypes.guess_type(source)
            # if no mime type is detected, result is None; we must change it
            mimetype = mimetype and mimetype or ''
            mediatype = self._get_mediatype(mimetype)
            alternate_text = obj.Title()
            caption = obj.Description()
            # we only include height and/or width if we have a value for them
            height = obj.getHeight()
            height = height and ' height="%s"' % obj.getHeight() or ''
            width = obj.getWidth()
            width = width and ' width="%s"' % obj.getWidth() or ''
            m = self.MEDIA % (mediatype,
                         mimetype, source, alternate_text, height, width,
                         caption)
            media.append(m)

        return media


class NewsML(View):
    """ Shows news article in NewsML XML format.
    """
    grok.context(INITF)
    grok.layer(INITFBrowserLayer)
    grok.name('newsml')
    grok.require('zope2.View')

    def version(self):
        """ Returns news article revision number.
        """
        # TODO: get revision number
        return 1

    def nitf_size(self):
        """ Returns size of the news article in NITF format.
        """
        # TODO: calculate size
        return 1000

    ITEM_REF = """
<itemRef href="%s/@@nitf" size="%s"
   contenttype="application/nitf+xml" format="fmt:nitf">
    <title>%s</title>
</itemRef>"""

    def get_related_items(self):
        """ Returns an itemRef tag for each related item (only News Articles).
        """
        items = getattr(self.context, 'relatedItems', None)
        if items is not None:
            related_items = []
            for i in items:
                href = i.to_object.absolute_url()
                size = self.nitf_size()
                title = i.to_object.Title()
                item_ref = self.ITEM_REF % (href, size, title)
                related_items.append(item_ref)
            return related_items


class Media(dexterity.DisplayForm):
    grok.context(INITF)
    grok.require('cmf.ModifyPortalContent')
