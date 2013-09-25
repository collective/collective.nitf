# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory

from plone.autoform.interfaces import WIDGETS_KEY
from zope import schema as _schema
from plone.app.relationfield.behavior import IRelatedItems

_ = MessageFactory('collective.nitf')


widget = 'collective.z3cform.widgets.multicontent_search_widget.MultiContentSearchFieldWidget'
_widget_values = IRelatedItems.queryTaggedValue(WIDGETS_KEY, {})
_widget_values['relatedItems'] = widget
IRelatedItems.setTaggedValue(WIDGETS_KEY, _widget_values)

_schema.getFields(IRelatedItems)['relatedItems'].index_name = 'Related Items'
