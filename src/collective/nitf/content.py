# -*- coding: utf-8 -*-
from collective.nitf.interfaces import INITF
from plone.app.textfield.interfaces import ITransformer
from plone.dexterity.content import Container
from plone.indexer import indexer
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implements


class NITF(Container):

    """A News Article based on the News Industry Text Format specification."""

    implements(INITF)

    def is_empty(self):
        """Return True if the container has no files nor links inside.
        """
        content_filter = {'portal_type': ['File', 'Link']}
        return not self.listFolderContents(content_filter)

    def get_images(self):
        """Return a list of image objects contained in the news article."""
        content_filter = {'portal_type': 'Image'}
        return self.listFolderContents(content_filter)

    # The purpose of these methods is to emulate those on News Item
    def getImage(self):
        """Return the first Image inside the News Article.
        """
        content_filter = {'portal_type': 'Image'}
        images = self.listFolderContents(content_filter)
        return images[0] if len(images) > 0 else None

    image = getImage  # XXX: a hack to support summary_view

    def imageCaption(self):
        image = self.getImage()
        if image is not None:
            return image.Description()

    def tag(self, **kwargs):
        # tag original implementation returns object title in both, alt and
        # title attributes
        image = self.getImage()
        if image is not None:
            scales = image.restrictedTraverse('@@images')
            if 'scale' in kwargs:
                scale_id = kwargs.get('scale')
                del kwargs['scale']
            else:
                scale_id = 'thumb'
            kwargs['alt'] = image.Description()
            kwargs['title'] = image.Title()
            scale = scales.scale(fieldname='image', scale=scale_id)
            return scale.tag(**kwargs)

    def image_thumb(self):
        """Return a thumbnail."""
        image = self.getImage()
        if image is not None:
            view = image.unrestrictedTraverse('@@images')
            # Return the data
            return view.scale(fieldname='image', scale='thumb').data


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
