# -*- coding: utf-8 -*-

from zope import schema

from z3c.form.browser.textlines import TextLinesFieldWidget
from zope.interface import Interface

from plone.app.registry.browser import controlpanel

from collective.nitf import _
from collective.nitf import config


class INITFSettings(Interface):
    """ Interface for the control panel form.
    """

    sections = schema.Set(
            title=_(u'Available Sections'),
            required=True,
            default=set(),
            value_type=schema.TextLine(title=_(u'Section')),)

    default_section = schema.Choice(
            title=_(u'Default Section'),
            vocabulary=u'collective.nitf.Sections',
            required=False,)

    possible_genres = schema.List(title=_(u'Elegible Genres'),
            description=_(u"Choose genres to use in the site"),
            required=False,
            value_type=schema.Choice(vocabulary=config.GENRES),)

    default_genre = schema.Choice(
            title=_(u'Default Genre'),
            vocabulary=config.GENRES,
            required=False,
            default=config.DEFAULT_GENRE,)

    default_urgency = schema.Choice(
            title=_(u'Default Urgency'),
            vocabulary=config.URGENCIES,
            required=False,
            default=config.DEFAULT_URGENCY,)


class NITFSettingsEditForm(controlpanel.RegistryEditForm):
    schema = INITFSettings
    label = _(u'NITF Settings')
    description = _(u'Here you can modify the settings for collective.nitf.')

    def updateFields(self):
        super(NITFSettingsEditForm, self).updateFields()
        self.fields['sections'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self):
        super(NITFSettingsEditForm, self).updateWidgets()
        self.widgets['sections'].rows = 8
        self.widgets['sections'].style = u'width: 30%;'


class NITFSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NITFSettingsEditForm
