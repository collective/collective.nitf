# -*- coding:utf-8 -*-

from five import grok

from Products.CMFPlone.interfaces import INonInstallable


class HiddenProfiles(grok.GlobalUtility):

    grok.implements(INonInstallable)
    grok.provides(INonInstallable)
    grok.name('collective.nitf')

    def getNonInstallableProfiles(self):
        profiles = ['collective.nitf:uninstall', ]
        return profiles
