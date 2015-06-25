# -*- coding: utf-8 -*-
from collective.cover.tiles.basic import BasicTile
from collective.cover.tiles.basic import IBasicTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.nitf import _
from collective.nitf.interfaces import INITF
from plone import api
from plone.autoform import directives as form
from plone.tiles.interfaces import ITileDataManager
from zope import schema
from zope.browserpage import ViewPageTemplateFile
from zope.interface import implements


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


class NITFTile(BasicTile):

    """A tile that shows information about a News Article."""

    implements(INITFTile)

    index = ViewPageTemplateFile('nitf.pt')
    is_configurable = True
    is_editable = True
    is_droppable = True

    short_name = _(u'msg_short_name_nitf', u'News Article')

    def accepted_ct(self):
        """Return a list of content types accepted by the tile."""
        return ['collective.nitf.content']

    def populate_with_object(self, obj):
        super(NITFTile, self).populate_with_object(obj)

        if INITF.providedBy(obj):
            data_mgr = ITileDataManager(self)
            data = data_mgr.get()
            data['subtitle'] = obj.subtitle
            data['section'] = obj.section
            image = obj.getImage()
            data['media_producer'] = image.Rights() if image is not None else ''
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

    @property
    def date(self):
        """Return the date of the object, localized."""
        date = super(NITFTile, self).Date()
        return api.portal.get_localized_time(date, long_format=True)
