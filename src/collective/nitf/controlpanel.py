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

    available_sections = schema.Set(
        title=_(u'Available Sections'),
        description=_(u"List of available sections in the site."),
        required=True,
        default=set(),
        value_type=schema.TextLine(title=_(u'Section')),
        )

    default_section = schema.Choice(
        title=_(u"Default Section"),
        vocabulary=u'collective.nitf.AvailableSections',
        required=False,
        )

    available_genres = schema.List(
        title=_(u"Available Genres"),
        description=_(u"Select the list of available genres in the site. "
                       "Genres indicate a nature, journalistic or "
                       "intellectual characteristic of items."),
        required=False,
        default=[],
        value_type=schema.Choice(vocabulary=u'collective.nitf.Genres'),
        )

    default_genre = schema.Choice(
        title=_(u"Default Genre"),
        vocabulary=u'collective.nitf.Genres',
        required=False,
        default=config.DEFAULT_GENRE,
        )

    default_urgency = schema.Choice(
        title=_(u"Default Urgency"),
        vocabulary=u'collective.nitf.Urgencies',
        required=False,
        default=config.DEFAULT_URGENCY,
        )

    relatable_content_types = schema.List(
        title=_(u"Relatable Content Types"),
        description=_(u"Only objects of these content types will be "
                       "listed in the related items widget."),
        required=False,
        default=config.DEFAULT_RELATABLE_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(vocabulary=u'plone.app.vocabularies.ReallyUserFriendlyTypes'),
        )


class NITFSettingsEditForm(controlpanel.RegistryEditForm):
    schema = INITFSettings
    label = _(u"NITF Settings")
    description = _(u"Here you can modify the settings for collective.nitf.")

    def updateFields(self):
        super(NITFSettingsEditForm, self).updateFields()
        self.fields['available_sections'].widgetFactory = TextLinesFieldWidget

    def updateWidgets(self):
        super(NITFSettingsEditForm, self).updateWidgets()
        self.widgets['available_sections'].rows = 8
        self.widgets['available_sections'].style = u'width: 30%;'


class NITFSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NITFSettingsEditForm
