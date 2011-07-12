# -*- coding: utf-8 -*-

"""
$Id$
"""

PROJECTNAME = 'collective.nitf'
CONTROLPANEL_ID = 'nitf-settings'

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from collective.nitf import _

PROPERTIES = SimpleVocabulary([
    SimpleTerm(value=u'Analysis',
               title=_(u'Analysis')),
    SimpleTerm(value=u'Archive-Material',
               title=_(u'Archive-Material')),
    SimpleTerm(value=u'Background',
               title=_(u'Background')),
    SimpleTerm(value=u'Current',
               title=_(u'Current')),
    SimpleTerm(value=u'Feature',
               title=_(u'Feature')),
    SimpleTerm(value=u'Forecast',
               title=_(u'Forecast')),
    SimpleTerm(value=u'History',
               title=_(u'History')),
    SimpleTerm(value=u'Obituary',
               title=_(u'Obituary')),
    SimpleTerm(value=u'Opinion',
               title=_(u'Opinion')),
    SimpleTerm(value=u'Polls-Surveys',
               title=_(u'Polls-Surveys')),
    SimpleTerm(value=u'Profile',
               title=_(u'Profile')),
    SimpleTerm(value=u'Results-Listings-Tables',
               title=_(u'Results-Listings-Tables')),
    SimpleTerm(value=u'Sidebar-Supporting-Info',
               title=_(u'Sidebar-Supporting-Info')),
    SimpleTerm(value=u'Summary',
               title=_(u'Summary')),
    SimpleTerm(value=u'Transcript-Verbatim',
               title=_(u'Transcript-Verbatim')),
    ])

HIGH = 1
NORMAL = 5
LOW = 8

URGENCIES = SimpleVocabulary([
    SimpleTerm(value=HIGH, title=_(u'High')),
    SimpleTerm(value=NORMAL, title=_(u'Normal')),
    SimpleTerm(value=LOW, title=_(u'Low')),
    ])

# defaults
DEFAULT_PROPERTY = u'Current'
DEFAULT_URGENCY = NORMAL
