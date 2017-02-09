# coding: utf-8
from collective.nitf import _
from collective.nitf.utils import section_default_value
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
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
        defaultFactory=section_default_value,
    )
