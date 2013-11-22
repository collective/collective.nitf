# -*- coding: utf-8 -*-

from collective.nitf import _
from collective.nitf import config
from plone.app.registry.browser import controlpanel
from zope import schema
from plone.directives import form

PORTALTYPES = 'plone.app.vocabularies.ReallyUserFriendlyTypes'


class INITFSettings(form.Schema):
    """ Interface for the control panel form.
    """
    form.widget(available_sections='z3c.form.browser.textlines.TextLinesFieldWidget')
    available_sections = schema.Set(
        title=_(u'Available Sections'),
        description=_(u'List of available sections in the site.'),
        required=True,
        default=set(),
        value_type=schema.TextLine(title=_(u'Section')),
    )

    default_section = schema.Choice(
        title=_(u'Default Section'),
        vocabulary=u'collective.nitf.AvailableSections',
        required=False,
    )

    available_genres = schema.List(
        title=_(u'Available Genres'),
        description=_(u'Select the list of available genres in the site. '
                      u'Genres indicate a nature, journalistic or '
                      u'intellectual characteristic of items.'),
        required=False,
        default=[],
        value_type=schema.Choice(vocabulary=u'collective.nitf.Genres'),
    )

    default_genre = schema.Choice(
        title=_(u'Default Genre'),
        vocabulary=u'collective.nitf.Genres',
        required=False,
        default=config.DEFAULT_GENRE,
    )

    default_urgency = schema.Choice(
        title=_(u'Default Urgency'),
        vocabulary=u'collective.nitf.Urgencies',
        required=False,
        default=config.DEFAULT_URGENCY,
    )

    relatable_content_types = schema.List(
        title=_(u'Relatable Content Types'),
        description=_(u'Only objects of these content types will be '
                      u'listed in the related items widget.'),
        required=False,
        default=config.DEFAULT_RELATABLE_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(vocabulary=PORTALTYPES),
    )


class NITFSettingsEditForm(controlpanel.RegistryEditForm):
    schema = INITFSettings
    label = _(u'NITF Settings')
    description = _(u'Here you can modify the settings for collective.nitf.')


class NITFSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NITFSettingsEditForm
