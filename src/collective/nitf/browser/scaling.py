# -*- coding: utf-8 -*-
from plone.namedfile.scaling import ImageScaling as BaseImageScaling


class ImageScaling(BaseImageScaling):

    """Adapter to deal with issues created by our fake image field."""

    def scale(
        self,
        fieldname=None,
        scale=None,
        height=None,
        width=None,
        direction="thumbnail",
        **parameters
    ):
        """Deal with issues created by our fake image field."""
        if fieldname != "image":
            return None

        image = self.context.image()
        if image is None:
            return None

        scales = image.restrictedTraverse("@@images")
        return scales.scale(fieldname, scale, height, width, direction, **parameters)

    def getImageSize(self, fieldname=None):
        """Deal with issues created by our fake image field."""
        if fieldname != "image":
            return (0, 0)

        image = self.context.image()
        if image is None:
            return (0, 0)

        return image.image.getImageSize()
