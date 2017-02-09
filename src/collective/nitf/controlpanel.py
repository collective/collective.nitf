# -*- coding: utf-8 -*-
from collective.nitf import _
from collective.nitf import config
from collective.nitf.config import DEFAULT_GENRE
from collective.nitf.config import DEFAULT_SECTION
from plone.app.registry.browser import controlpanel
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema


PORTALTYPES = 'plone.app.vocabularies.ReallyUserFriendlyTypes'


class INITFSettings(model.Schema):
    """ Interface for the control panel form.
    """
    form.widget(available_sections='z3c.form.browser.textlines.TextLinesFieldWidget')
    available_sections = schema.Set(
        title=_(u'Available Sections'),
        description=_(u'List of available sections in the site.'),
        required=True,
        default=set([DEFAULT_SECTION]),
        value_type=schema.TextLine(title=_(u'Section')),
    )

    default_section = schema.Choice(
        title=_(u'Default Section'),
        description=_(u'Section to be used as default on new items.'),
        required=True,
        vocabulary=u'collective.nitf.AvailableSections',
        default=DEFAULT_SECTION,
    )

    available_genres = schema.List(
        title=_(u'Available Genres'),
        description=_(u'Select the list of available genres in the site. '
                      u'Genres indicate a nature, journalistic or '
                      u'intellectual characteristic of items.'),
        required=True,
        default=[DEFAULT_GENRE],
        value_type=schema.Choice(vocabulary=u'collective.nitf.Genres'),
    )

    default_genre = schema.Choice(
        title=_(u'Default Genre'),
        description=_(u'Genre to be used as default on new items.'),
        required=True,
        vocabulary=u'collective.nitf.Genres',
        default=DEFAULT_GENRE,
    )

    default_urgency = schema.Choice(
        title=_(u'Default Urgency'),
        vocabulary=u'collective.nitf.Urgencies',
        required=True,
        default=config.DEFAULT_URGENCY,
    )


class NITFSettingsEditForm(controlpanel.RegistryEditForm):
    schema = INITFSettings
    label = _(u'NITF Settings')
    description = _(u'Here you can modify the settings for collective.nitf.')


class NITFSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NITFSettingsEditForm
