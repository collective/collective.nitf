# -*- coding: utf-8 -*-
from collective.cover.tiles.basic import BasicTile
from collective.cover.tiles.basic import IBasicTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.nitf import _
from collective.nitf.config import NOT_RENDERED_ANONYMOUS_TILE_TOKEN
from collective.nitf.interfaces import INITF
from plone import api
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from zope import schema
from zope.browserpage import ViewPageTemplateFile
from zope.interface import implementer


class INITFTile(IBasicTile):

    """A tile that shows information about a News Article."""

    subtitle = schema.Text(
        title=_(u'Subtitle'),
        required=False,
    )

    form.omitted('section')
    form.no_omit(IDefaultConfigureForm, 'section')
    section = schema.Text(
        title=_(u'Section'),
        required=False,
    )

    media_producer = schema.TextLine(
        # nitf/body/body.content/media/media-producer
        title=_(u'Image Rights'),
        required=False,
    )


@implementer(INITFTile)
class NITFTile(BasicTile):

    """A tile that shows information about a News Article."""

    index = ViewPageTemplateFile('nitf.pt')
    is_configurable = True
    is_editable = True
    is_droppable = True

    short_name = _(u'msg_short_name_nitf', u'News Article')

    def __call__(self, *args, **kwargs):
        """
        This method was inspired by

            https://github.com/plone/plone.tiles/blob/5f13cc63efc3c0ee429ff103685b19161333afd7/plone/tiles/esi.py#L59

        Based on ConditionalESIRendering, if there's no index, 'render' is
        called instead. We used the same idea but for a different purpose: if
        the object related to the tile isn't available (happens when an
        anonymous user tries to view an unpublished item in a tile), we show
        a message saying that there's a privilege problem. If the tile is
        available, __call__ is normally called.
        """
        if api.user.is_anonymous() and self.brain is None and not self.is_compose_mode():
            # XXX: We can't return an empty string or
            # 'Tile content replaced during the blocks transform.'
            # will be shown. Usually, when an empty string is rendered from a
            # tile means an error (like Internal Server Error) and render_section
            # https://github.com/collective/collective.cover/blob/445db248ac5e10cb54d3bcc70fb3a8b9381d4730/src/collective/cover/browser/layout.py#L131
            # renders this default message. To avoid messing up with the
            # expectation of 'Tile content replaced during the blocks transform.'
            # being usually shown when there's a problem, we'll return a
            # harmless span.
            return NOT_RENDERED_ANONYMOUS_TILE_TOKEN
        else:
            return super(NITFTile, self).__call__(*args, **kwargs)

    def accepted_ct(self):
        """Return a list of content types accepted by the tile."""
        return ['collective.nitf.content']

    def populate_with_object(self, obj):
        super(BasicTile, self).populate_with_object(obj)

        if INITF.providedBy(obj):
            image = obj.image()
            data = dict(
                title=obj.title,
                description=obj.description,
                subtitle=obj.subtitle,
                section=obj.section,
                uuid=IUUID(obj),
                date=True,
                subjects=True,
                image=self.get_image_data(image),
                media_producer=obj.media_producer(),
            )
            # clear scales as new image is getting saved
            self.clear_scales()

            data_mgr = ITileDataManager(self)
            data_mgr.set(data)

    def _get_field_configuration(self, field):
        """Return a dict with the configuration of the field. This is a
        helper function to deal with the ugliness of the internal data
        structure.
        """
        fields = self.get_configured_fields()
        return [f for f in fields if f['id'] == field][0]

    @property
    def title_tag(self):
        field = self._get_field_configuration('title')
        tag, title, href = field['htmltag'], field['content'], self.getURL()
        return u"""
            <{tag}>
              <a href="{href}">{title}</a>
            </{tag}>
            """.format(tag=tag, title=title, href=href)
