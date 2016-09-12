# -*- coding: utf-8 -*-
"""The News Article content type.

We have to deal with issues created by a fake image field on it.
Note that methods in this class can not be declared as properties
(acquisition chain is lost).
"""
from collective.nitf.interfaces import INITF
from plone.app.textfield.interfaces import ITransformer
from plone.dexterity.content import Container
from plone.indexer import indexer
from Products.CMFPlone.utils import safe_unicode
from zope.deprecation import deprecation
from zope.interface import implementer


@implementer(INITF)
class NITF(Container):

    """A News Article based on the News Industry Text Format specification."""

    def is_empty(self):
        """Check if the container has no files nor links inside."""
        content_filter = {'portal_type': ['File', 'Link']}
        return not self.listFolderContents(content_filter)

    def get_images(self):
        """Return a list of images contained in the News Article."""
        content_filter = {'portal_type': 'Image'}
        return self.listFolderContents(content_filter)

    def image(self):
        """Return the first image."""
        images = self.get_images()
        return images[0] if len(images) > 0 else None

    def media_caption(self):
        """Return the description of the first image."""
        try:
            return self.image().Description()
        except AttributeError:
            return u''

    def media_producer(self):
        """Return the author of the first image."""
        try:
            return self.image().Rights()
        except AttributeError:
            return u''

    # XXX: emulate News Item methods and
    #      deal with issues created by our fake image field

    @deprecation.deprecate('getImage() is deprecated; use image().')
    def getImage(self):
        return self.image()

    @deprecation.deprecate('imageCaption() is deprecated; use media_caption.')
    def imageCaption(self):
        return self.media_caption()

    image_thumb = image

    def tag(self, **kwargs):
        try:
            scales = self.image().restrictedTraverse('@@images')
            return scales.tag('image', **kwargs)
        except AttributeError:
            return None


@indexer(INITF)
def textIndexer(obj):
    """SearchableText contains id, title, subtitle, abstract, author and body
    text as plain text.
    """
    transformer = ITransformer(obj)
    text = obj.text
    if text:
        text = transformer(obj.text, 'text/plain')

    searchable_text = [safe_unicode(entry) for entry in (
        obj.id,
        obj.Title(),
        obj.subtitle,
        obj.Description(),
        obj.byline,
        text,
        obj.location,
    ) if entry]

    return u' '.join(searchable_text)
