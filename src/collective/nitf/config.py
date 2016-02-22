# -*- coding: utf-8 -*-
from collective.nitf import _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


PROJECTNAME = 'collective.nitf'

# this cames from http://cv.iptc.org/newscodes/genre/
GENRES = SimpleVocabulary([
    SimpleTerm(value=u'Actuality',
               title=_(u'Actuality')),
    # Definition: The object contains the recording of the event.
    SimpleTerm(value=u'Advice',
               title=_(u'Advice')),
    # Definition: The object contains advice, typically letters and answers
    # about personal problems, that are publishable.
    SimpleTerm(value=u'Almanac',
               title=_(u'Almanac')),
    # Definition: List of data, including birthdays of famous people and items
    # of historical significance, for a given day.
    SimpleTerm(value=u'Analysis',
               title=_(u'Analysis')),
    # Definition: The object contains data and conclusions drawn by a
    # journalist who has researched the story in depth.
    SimpleTerm(value=u'Anniversary',
               title=_(u'Anniversary')),
    # Definition: Stories about the anniversary of some important event that
    # took place in recent history, usually bringing a short review of the
    # event itself.
    SimpleTerm(value=u'Archive material',
               title=_(u'Archive material')),
    # Definition: The object contains material distributed previously that has
    # been selected from the originator's archives.
    SimpleTerm(value=u'Background',
               title=_(u'Background')),
    # Definition: The object provides some scene setting and explanation for
    # the event being reported.
    SimpleTerm(value=u'Current',
               title=_(u'Current')),
    # Definition: The object content is about events taking place at the time
    # of the report.
    SimpleTerm(value=u'Curtain Raiser',
               title=_(u'Curtain Raiser')),
    # Definition: The object contains information about the staging and outcome
    # of an immediately upcoming event.
    SimpleTerm(value=u'Daybook',
               title=_(u'Daybook')),
    # Definition: Items filed on a regular basis that are lists of upcoming
    # events with time and place, designed to inform others of events for
    # planning purposes.
    SimpleTerm(value=u'Exclusive',
               title=_(u'Exclusive')),
    # Definition: Information content, in any form, that is unique to a
    # specific information provider.
    SimpleTerm(value=u'Feature',
               title=_(u'Feature')),
    # Definition: The object content is about a particular event or individual
    # that may not be significant to the current breaking news.
    SimpleTerm(value=u'Fixture',
               title=_(u'Fixture')),
    # Definition: The object contains data that occurs often and predictably.
    SimpleTerm(value=u'Forecast',
               title=_(u'Forecast')),
    # Definition: The object contains opinion as to the outcome of a future
    # event.
    SimpleTerm(value=u'From the Scene',
               title=_(u'From the Scene')),
    # Definition: The object contains a report from the scene of an event.
    SimpleTerm(value=u'History',
               title=_(u'History')),
    # Definition: The object content is based on previous rather than current
    # events.
    SimpleTerm(value=u'Horoscope',
               title=_(u'Horoscope')),
    # Definition: Astrological forecasts
    SimpleTerm(value=u'Interview',
               title=_(u'Interview')),
    # Definition: The object contains a report of a dialogue with a news source
    # that gives it significant voice (includes Q and A).
    SimpleTerm(value=u'Music',
               title=_(u'Music')),
    # Definition: The object contains music alone.
    SimpleTerm(value=u'Obituary',
               title=_(u'Obituary')),
    # Definition: The object contains a narrative about an individual's life
    # and achievements for publication after his or her death.
    SimpleTerm(value=u'Opinion',
               title=_(u'Opinion')),
    # Definition: The object contains an editorial comment that reflects the
    # views of the author.
    SimpleTerm(value=u'Polls and Surveys',
               title=_(u'Polls and Surveys')),
    # Definition: The object contains numeric or other information produced as
    # a result of questionnaires or interviews.
    SimpleTerm(value=u'Press Release',
               title=_(u'Press Release')),
    # Definition: The object contains promotional material or information
    # provided to a news organisation.
    SimpleTerm(value=u'Press-Digest',
               title=_(u'Press-Digest')),
    # Definition: The object contains an editorial comment by another medium
    # completely or in parts without significant journalistic changes.
    SimpleTerm(value=u'Profile',
               title=_(u'Profile')),
    # Definition: The object contains a description of the life or activity of
    # a news subject (often a living individual).
    SimpleTerm(value=u'Program',
               title=_(u'Program')),
    # Definition: A news item giving lists of intended events and time to be
    # covered by the news provider. Each program covers a day, a week, a month
    # or a year. The covered period is referenced as a keyword.
    SimpleTerm(value=u'Question and Answer Session',
               title=_(u'Question and Answer Session')),
    # Definition: The object contains the interviewer and subject questions and
    # answers.
    SimpleTerm(value=u'Quote',
               title=_(u'Quote')),
    # Definition: The object contains a one or two sentence verbatim in direct
    # quote.
    SimpleTerm(value=u'Raw Sound',
               title=_(u'Raw Sound')),
    # Definition: The object contains unedited sounds.
    SimpleTerm(value=u'Response to a Question',
               title=_(u'Response to a Question')),
    # Definition: The object contains a reply to a question.
    SimpleTerm(value=u'Results Listings and Statistics',
               title=_(u'Results Listings and Statistics')),
    # Definition: The object contains alphanumeric data suitable for
    # presentation in tabular form.
    SimpleTerm(value=u'Retrospective',
               title=_(u'Retrospective')),
    # Definition: The object contains material that looks back on a specific
    # (generally long) period of time such as a season, quarter, year or
    # decade.
    SimpleTerm(value=u'Review',
               title=_(u'Review')),
    # Definition: The object contains a critique of a creative activity or
    # service (for example a book, a film or a restaurant).
    SimpleTerm(value=u'Scener',
               title=_(u'Scener')),
    # Definition: The object contains a description of the event circumstances.
    SimpleTerm(value=u'Side bar and supporting information',
               title=_(u'Side bar and supporting information')),
    # Definition: The object contains a related story that provides additional
    # insight into the news event being reported.
    SimpleTerm(value=u'Special Report',
               title=_(u'Special Report')),
    # Definition: In-depth examination of a single subject requiring extensive
    # research and usually presented at great length, either as a single item
    # or as a series of items.
    SimpleTerm(value=u'Summary',
               title=_(u'Summary')),
    # Definition: The object contains a single item synopsis of a number of
    # news stories (generally unrelated).
    SimpleTerm(value=u'Synopsis',
               title=_(u'Synopsis')),
    # Definition: The object contains a condensed version of a single news
    # item.
    SimpleTerm(value=u'Text only',
               title=_(u'Text only')),
    # Definition: The object contains a transcription of text.
    SimpleTerm(value=u'Transcript and Verbatim',
               title=_(u'Transcript and Verbatim')),
    # Definition: The object contains a word for word report of a discussion or
    # briefing without significant journalistic intervention.
    SimpleTerm(value=u'Update',
               title=_(u'Update')),
    # Definition: The object contains an intraday snapshot (as for electronic
    # services) of a single news subject.
    SimpleTerm(value=u'Voicer',
               title=_(u'Voicer')),
    # Definition: The object contains only voice.
    SimpleTerm(value=u'Wrap',
               title=_(u'Wrap')),
    # Definition: The object contains a complete summary of the event.
    SimpleTerm(value=u'Wrapup',
               title=_(u'Wrapup')),
    # Definition: The object contains a recap of a running story (such as the
    # end of the day).
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
DEFAULT_GENRE = u'Current'
DEFAULT_SECTION = _(u'General')
DEFAULT_URGENCY = NORMAL

# Cycle2 JS resources used by the package
JS_RESOURCES = (
    '++resource++collective.js.cycle2/jquery.cycle2.min.js',
    '++resource++collective.js.cycle2/jquery.cycle2.carousel.min.js',
    '++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js',
)
