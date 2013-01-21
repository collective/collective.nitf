# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from uuid import uuid3
from uuid import NAMESPACE_OID

from DateTime import DateTime

from zope.component import adapts
from zope.interface import implements

from collective.nitf import _
from collective.nitf.controlpanel import INITFSettings
from collective.z3cform.widgets.multicontent_search_widget import (
    MultiContentSearchFieldWidget,
)
from five import grok
from plone.app.dexterity.behaviors.metadata import IDublinCore
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.app.textfield.value import RichTextValue
from plone.dexterity.content import Container
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.indexer import indexer
from plone.registry.interfaces import IRegistry

from plone.uuid.interfaces import IUUID

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from z3c.relationfield.schema import (
    RelationChoice,
    RelationList,
)
from zope import schema
from zope.component import getUtility

from zope.cachedescriptors.property import Lazy as lazy_property

try:
    # We have collective.syndication
    from collective.syndication.adapters import BaseNewsMLItem
    
    from collective.syndication.interfaces import INewsMLSyndicatable
    from collective.syndication.interfaces import INewsMLFeed
    HAS_C_SYNDICATION = True
except:
    # We don't have collective.syndication
    from collective.nitf.interfaces import INewsMLFeed
    from collective.nitf.interfaces import INewsMLSyndicatable
    from collective.nitf.utils import cleanup_body_html
    HAS_C_SYNDICATION = False


class INITF(form.Schema):
    """A news item based on the News Industry Text Format specification.
    """

    #title = schema.TextLine()
        # nitf/head/title and nitf/body/body.head/hedline/hl1

    form.order_after(subtitle='IDublinCore.title')
    subtitle = schema.TextLine(
        # nitf/body/body.head/hedline/hl2
        title=_(u'Subtitle'),
        description=_(u'help_subtitle',
                      default=u'A subordinate headline for the article.'),
        default=u'',
        missing_value=u'',
        required=False,
    )

    #description = schema.Text()
        # nitf/body/body.head/abstract

    byline = schema.TextLine(
        # nitf/body/body.head/byline/person
        title=_(u'Author'),
        default=u'',
        missing_value=u'',
        required=False,
    )

    text = RichText(
        # nitf/body/body.content
        title=_(u'Body text'),
        default=RichTextValue(u''),
        missing_value=RichTextValue(u''),
        required=False,
    )

    genre = schema.Choice(
        # nitf/head/tobject/tobject.property/@tobject.property.type
        title=_(u'Genre'),
        description=_(u'help_genre',
                      default=u'Describes the nature, journalistic or '
                              u'intellectual characteristic of a news '
                              u'object, not specifically its content.'),
        source=u'collective.nitf.AvailableGenres',
    )

    section = schema.Choice(
        # nitf/head/pubdata/@position.section
        title=_(u'Section'),
        description=_(u'help_section',
                      default=u'Named section where the article will '
                              u'appear.'),
        vocabulary=u'collective.nitf.AvailableSections',
    )

    urgency = schema.Choice(
        # nitf/head/docdata/urgency/@ed-urg
        title=_(u'Urgency'),
        description=_(u'help_urgency',
                      default=u'News importance.'),
        vocabulary=u'collective.nitf.Urgencies',
    )

    # XXX: this field uses a special widget that access the most recent items
    # of content types defined in the control panel; see browser.py and
    # controlpanel.py for more information
    relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        missing_value=[],
        value_type=RelationChoice(title=u"Related",
                                  source=ObjPathSourceBinder()),
        required=False,
    )
    form.widget(relatedItems=MultiContentSearchFieldWidget)

    location = schema.TextLine(
        # nitf/body/body.head/dateline/location
        title=_(u'Location'),
        description=_(u'help_location',
                      default=u'Event location. Where an event took '
                              u'place (as opposed to where the story was '
                              u'written).'),
        default=u'',
        missing_value=u'',
        required=False,
    )

    form.fieldset(
        'categorization',
        label=_(u'Categorization'),
        fields=['relatedItems', 'section', 'urgency', 'genre', 'subjects',
                'language'],
    )


class NITF(Container):
    grok.implements(INITF)

    def _get_brains(self, object_name=None):
        """ Return a list of brains inside the NITF object.
        """
        catalog = getToolByName(self, 'portal_catalog')
        path = '/'.join(self.getPhysicalPath())
        brains = catalog(Type=object_name, path=path,
                         sort_on='getObjPositionInParent')

        return brains

    def get_images(self):
        """ Return a list of image brains inside the NITF object.
        """
        return self._get_brains('Image')

    def has_images(self):
        """ Return the number of images inside the NITF object.
        """
        return len(self.get_images())

    def get_files(self):
        """ Return a list of file brains inside the NITF object.
        """
        return self._get_brains('File')

    def has_files(self):
        """ Return the number of files inside the NITF object.
        """
        return len(self.get_files())

    def get_links(self):
        """ Return a list of link brains inside the NITF object.
        """
        return self._get_brains('Link')

    def has_links(self):
        """ Return the number of links inside the NITF object.
        """
        return len(self.get_links())

    def get_media(self):
        """ Return a list of object brains inside the NITF object.
        """
        media_ct = [x.title for x in self.allowedContentTypes()]
        return self._get_brains(media_ct)

    def has_media(self):
        """ Return the number of media inside the NITF object.
        """
        return len(self.get_media())
    
    def getText(self):
        return self.text.output

    # The purpose of these methods is to emulate those on News Item
    def getImage(self):
        images = self.get_images()
        if len(images) > 0:
            return images[0].getObject()
        return None

    def imageCaption(self):
        image = self.getImage()
        if image is not None:
            return image.Description()

    def tag(self, **kwargs):
        # tag original implementation returns object title in both, alt and
        # title attributes
        image = self.getImage()
        if image is not None:
            return image.tag(**kwargs)


@form.default_value(field=INITF['genre'])
def genre_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_genre


@form.default_value(field=INITF['section'])
def section_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_section


@form.default_value(field=INITF['urgency'])
def urgency_default_value(data):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(INITFSettings)
    return settings.default_urgency


# TODO: move this to Dexterity's core
@form.default_value(field=IDublinCore['language'])
def language_default_value(data):
    """ Returns portal's default language or None.
    """
    portal_properties = getToolByName(data, "portal_properties", None)
    if portal_properties is not None:
        site_properties = getattr(portal_properties, 'site_properties', None)
        if site_properties is not None:
            if site_properties.hasProperty('default_language'):
                return site_properties.getProperty('default_language')


@indexer(INITF)
def textIndexer(obj):
    """SearchableText contains id, title, subtitle, abstract, author and body
    text as plain text.
    """
    transformer = ITransformer(obj)
    text = transformer(obj.text, 'text/plain')

    searchable_text = [safe_unicode(entry) for entry in (
        obj.id,
        obj.Title(),
        obj.subtitle,
        obj.Description(),
        obj.byline,
        text,
        obj.location,
    )]

    return u" ".join(searchable_text)

grok.global_adapter(textIndexer, name='SearchableText')


if HAS_C_SYNDICATION:
    class NITFNewsMLItem(BaseNewsMLItem):
        implements(INewsMLSyndicatable)
        adapts(INITF, INewsMLFeed)

        @property
        def image_url(self):
            if self.has_image:
                img = self.context.getImage()
                # Support up to 768px max size
                url = "%s/image_large" % img.absolute_url()
                return url

        @lazy_property
        def author(self):
            return self.context.byline
else:
    class NITFNewsMLItem(object):
        implements(INewsMLSyndicatable)
        adapts(INITF, INewsMLFeed)

        def __init__(self, context, feed):
            self.context = context
            self.feed = feed
            
        @property
        def title(self):
            return self.context.Title()

        @property
        def description(self):
            return self.context.Description()
        
        @property
        def uid(self):
            uuid = IUUID(self.context, None)
            if uuid is None and hasattr(self.context, 'UID'):
                return self.context.UID()
            return uuid
        
        @property
        def published(self):
            date = self.context.EffectiveDate()
            if date and date != 'None':
                return DateTime(date)

        @property
        def modified(self):
            date = self.context.ModificationDate()
            if date:
                return DateTime(date)
            
        @property
        def image_url(self):
            if self.has_image:
                img = self.context.getImage()
                # Support up to 768px max size
                url = "%s/image_large" % img.absolute_url()
                return url

        @lazy_property
        def author(self):
            return self.context.byline
            
        # TODO: This method will use lxml instead of BeautifulSoup to clean
        #       the HTML, leaving it here for the future.
        #@property
        #def body(self):
            #body = self.context.getText()
            
            #if body:
                #html = fromstring(body)
                #cleanup_body_html(html)

                ## lxml puts everything inside a <div>. Workaround that here
                #if html.tag == 'div':
                    #result = ''.join([tostring(i).strip() for i in html])
                #else:
                    #result = tostring(html)
                    
                #return result
        
        @property
        def body(self):
            body = self.context.getText()
            result = ""

            if body:
                # valid_tags = ['p', 'ul', 'hedline', 'hl1', 'media']

                soup = BeautifulSoup(body)

                for tag in soup.findAll(True):
                    attrs = dict()
                    # Remove all attributes, except hrefs
                    if 'href' in tag.attrs:
                        attrs['href'] = tag.attrs['href']

                    tag.attrs = attrs

                    # Now replace some common tags
                    if tag.name == 'h2':
                        tag.name = 'p'
                    elif tag.name == 'span':
                        tag.unwrap()
                    elif tag.name == 'ol':
                        tag.name = 'ul'

                if soup.find('body'):
                    result = soup.body.renderContents()
                else:
                    result = str(soup)

                # Remove some whitespace
                result = result.replace('\n', '')
                result.strip()

            return result

        @lazy_property
        def site_url(self):
            return self.feed.site_url

        @property
        def image_mime_type(self):
            if self.has_image:
                img = self.context.getImage()
                return img.content_type

        @property
        def image_title(self):
            result = ''
            if self.has_image:
                caption = getattr(self.context, 'imageCaption', None)
                if caption and caption != '':
                    result = caption
                else:
                    result = self.title
            return result

        @property
        def has_image(self):
            result = False
            img = getattr(self.context, 'getImage', None)
            if img:
                img_contents = img()
                result = img_contents and img_contents != ''
            return result

        def duid(self, value):
            uid = uuid3(NAMESPACE_OID, self.uid + str(value))
            return uid.hex
            
        @property
        def created(self):
            return self.context.created()
