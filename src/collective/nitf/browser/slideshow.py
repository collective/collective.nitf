# -*- coding: utf-8 -*-
from collective.nitf.browser import View

import json


class SlideshowView(View):

    """Slideshow view for a News Article."""

    def imagesJson(self):
        """ """
        try:
            img_brains = self.get_images()
        except IndexError:
            img_brains = None
        if img_brains:
            data = [{'image': str(brain.getPath() + '/image_preview'),
                     'title': brain.Title,
                     'description': brain.Description, 'right': brain.Rights(),
                     'link': brain.getURL()} for brain in img_brains]
        else:
            data = []

        return json.dumps(data)
