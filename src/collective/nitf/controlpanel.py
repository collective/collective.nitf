# -*- coding: utf-8 -*-
from collective.nitf import _
from collective.nitf import config
from plone.app.registry.browser import controlpanel
from z3c.form.browser.textlines import TextLinesFieldWidget
from zope import schema
from zope.interface import Interface

PORTALTYPES = 'plone.app.vocabularies.ReallyUserFriendlyTypes'


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
                      u"Genres indicate a nature, journalistic or "
                      u"intellectual characteristic of items."),
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
                      u"listed in the related items widget."),
        required=False,
        default=config.DEFAULT_RELATABLE_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(vocabulary=PORTALTYPES),
    )

    show_title_counter = schema.Bool(
        title=_(u"label_show_title_counter",
                default=u"Show Title characters counter"),
        description=_(u"help_show_title_counter",
                      default=u"If selected, the title is going to provide a character counter"),
        required=False,
        default=False,
    )

    title_max_chars = schema.Int(
        title=_(u"label_title_max_chars",
                default=u"Max number of characters acepted by the title"),
        description=_(u"help_title_max_chars",
                      default=u"This limit is just visual, does not enforce validation"),
        default=140,
        required=False,
    )

    title_optimal_chars = schema.Int(
        title=_(u"label_title_optimal_chars",
                default=u"Optimal number of characters for the nitf title"),
        description=_(u"help_title_max_chars",
                      default=u"The optimal value is going to be the range between this value and the max"),
        default=140,
        required=False,
    )

    show_description_counter = schema.Bool(
        title=_(u"label_show_description_counter",
                default=u"Show Description characters counter"),
        description=_(u"help_show_description_counter",
                      default=u"If selected, the description is going to provide a character counter"),
        required=False,
        default=False,
    )

    description_max_chars = schema.Int(
        title=_(u"label_description_max_chars",
                default=u"Max number of characters acepted by the description"),
        description=_(u"help_description_max_chars",
                      default=u"This limit is just visual, does not enforce validation"),
        default=140,
        required=False,
    )

    description_optimal_chars = schema.Int(
        title=_(u"label_description_optimal_chars",
                default=u"Optimal number of characters for the nitf description"),
        description=_(u"help_description_max_chars",
                      default=u"The optimal value is going to be the range between this value and the max"),
        default=140,
        required=False,
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
