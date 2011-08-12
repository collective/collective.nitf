# -*- coding: utf-8 -*-

"""
$Id$
"""

import random
from StringIO import StringIO
import logging

# TODO: mover el logger a un layer que afecte solo al transmogrifier
logging.basicConfig()
logger = logging.getLogger('collective.nitf')

from zope.event import notify
from zope.lifecycleevent import ObjectAddedEvent
from zope.lifecycleevent import ObjectCreatedEvent
from Products.PloneTestCase import ptc
from plone.app.textfield.value import RichTextValue
import collective.testcaselayer.ptc
from plone.dexterity.utils import createContent
ptc.setupPloneSite()

zptlogo = (
    'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
    '\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
    '\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
    '\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
    '\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
    '\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
    '\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
    '\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
    '\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
    '\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
    '\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
    '\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
    '\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
    '\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
    '\x00A\x00;'
    )


class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        # Install the collective.nitf product
        self.addProfile('collective.nitf:default')

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])


class MigrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        # Install the collective.nitf product
        self.addProfile('collective.nitf:default')
        #self.loginAsPortalOwner()
        self.login()
        self.populateContainer(self.folder)
        self.portal._delObject('front-page')

    def populateContainer(self, container, default_type='News Item', limit=4):
        for n in range(0, limit):
            n_id = 'n%s' % str(n + 1)
            #context = createContent('collective.nitf.content',
            #                        id=n_id,
            #                        title=u'News %s' % str(n+1),
            #                        description=u'Description %s' % str(n+1),
            #                        subject=(u"Category 1", u"Category 2", u"A third category"))
            #notify(ObjectCreatedEvent(context))
            #container[n_id] = context
            container.invokeFactory(default_type,
                                    id=n_id,
                                    title=u'News %s' % str(n + 1),
                                    description=u'Description %s' % str(n + 1),
                                    subject=(u"Category 1", u"Category 2", u"A third category")
                                    )
            notify(ObjectAddedEvent(container[n_id]))
            #container[n_id].setTitle(u'News %s' % str(n+1))
            #container[n_id].setDescription(u'Description %s' % str(n+1))
            #container[n_id].setSubject((u"Category 1", u"Category 2", u"A third category"))
            if default_type == 'News Item':
                container[n_id].setText(u'News %s' % str(n + 1))
                # Randomly sets images on news items
                if random.choice([True, False]):
                    container[n_id].setImage(StringIO(zptlogo))
                    container[n_id].setImageCaption(u'Zope LOGO %s' % str(n + 1))
                logger.debug(u"Populating: %s %s %s" % (default_type, n_id, container[n_id].getImage()))
            if default_type == 'collective.nitf.content':
                container[n_id].body = RichTextValue(u'<p>News %s</p>' % str(n + 1),
                                        'text/html', 'text/x-html-safe')
                logger.debug(u"Populating: %s %s %s" % (default_type, n_id, container[n_id].objectIds()))
            container[n_id].reindexObject()


MigrationLayer = MigrationTestLayer([collective.testcaselayer.ptc.ptc_layer])


class BrowserTestLayer(MigrationTestLayer):

    def afterSetUp(self):
        # Install the collective.nitf product
        self.addProfile('collective.nitf:default')
        self.logo = zptlogo
        self.login()
        self.populateContainer(self.folder, 'collective.nitf.content')
        for nitf in self.folder.values():
            self.add_image(nitf, "zlogo1.gif")
            self.add_image(nitf, "zlogo2.gif")
            nitf.reindexObject()

    def add_image(self, container, m_id):
        container.invokeFactory('Image', id=m_id, title=u"Logo GIF",
                                image=StringIO(zptlogo))


BrowserLayer = BrowserTestLayer([collective.testcaselayer.ptc.ptc_layer])