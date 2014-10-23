# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.nitf.browser import View
from plone.uuid.interfaces import IUUID

import mimetypes


class NITF(View):

    """Shows news article in NITF XML format."""

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
            m = self.MEDIA % (mediatype, mimetype, source, alternate_text,
                              height, width, caption)
            media.append(m)

        return media
