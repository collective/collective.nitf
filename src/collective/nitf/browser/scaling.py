# -*- coding: utf-8 -*-
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling
from Products.CMFPlone.utils import safe_hasattr
from zope.traversing.interfaces import TraversalError


class ImageScaling(BaseImageScaling):

    """Adapter to deal with issues created by our fake image field."""

    def traverse(self, name, furtherPath):
        """Fix image generation using traversal. The only valid option
        for image field name is "image"; that's the difference with
        the original code. We need to find out later if this is a bug
        in plone.app.imaging or not.

        See: https://github.com/collective/collective.nitf/pull/171
        """
        if not furtherPath:
            if safe_hasattr(self, '_image_fieldname'):
                scale_name = name
                name = self._image_fieldname
            else:
                scale_name = None
            image = self.scale(name, scale_name)
            if image is not None:
                return image.tag()
            raise TraversalError(self, name)
        if name == 'image':
            self._image_fieldname = name
            return self
        raise TraversalError(self, name)

    def scale(self, fieldname=None, scale=None, height=None, width=None, **kwargs):
        """Fix image generation on summary_view in collections."""
        if fieldname == 'image':
            image = self.context.image()
            scales = image.restrictedTraverse('@@images')
            return scales.scale(fieldname, scale, height, width, **kwargs)
        else:
            # XXX: check if we're getting here at some point
            return super(ImageScaling, self).scale(
                fieldname, scale, height, width, **kwargs)
