# coding: utf-8
from collective.nitf import _
from collective.nitf.controlpanel import INITFSettings
from plone.directives import form
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from zope import schema
from zope.component import getUtility
from zope.interface import provider


@provider(form.IFormFieldProvider)
class ISection(model.Schema):

    """Behavior interface to make a content type support sections."""

    model.fieldset('categorization', fields=['section'])
    form.order_before(section='genre')

    # nitf/head/pubdata/@position.section
    section = schema.Choice(
        title=_(u'Section'),
        description=_(
            u'help_section',
            default=u'Named section where the item will appear.',
        ),
        vocabulary=u'collective.nitf.AvailableSections',
    )


@form.default_value(field=ISection['section'])
def section_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_section
