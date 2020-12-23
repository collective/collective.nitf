# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '2.1.0'
description = "A content type inspired on the IPTC's News Industry Text Format specification."
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='collective.nitf',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone :: Addon',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: JavaScript',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Office/Business :: News/Diary',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='plone dexterity iptc newsml nitf',
      author='Hector Velarde',
      author_email='hector.velarde@gmail.com',
      url='https://github.com/collective/collective.nitf',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'Acquisition',
          'collective.js.jqueryui',
          'collective.prettydate >=1.1',
          'plone.api',
          'plone.app.content',
          'plone.app.contentmenu',
          'plone.app.dexterity [relations]',
          'plone.app.imaging',
          'plone.app.layout >=2.3.12',
          'plone.app.lockingbehavior',
          'plone.app.portlets',
          'plone.app.registry',
          'plone.app.relationfield',
          'plone.app.textfield',
          'plone.app.upgrade',
          'plone.app.vocabularies',
          'plone.autoform',
          'plone.behavior',
          'plone.dexterity',
          'plone.formwidget.autocomplete',
          'plone.formwidget.contenttree',
          'plone.indexer',
          'plone.memoize',
          'plone.portlets',
          'plone.registry',
          'plone.supermodel',
          'plone.uuid',
          'Products.CMFPlone >=4.3',
          'Products.CMFQuickInstallerTool',
          'Products.GenericSetup',
          'setuptools',
          'zope.browserpage',
          'zope.component',
          'zope.deprecation',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'AccessControl',
              'lxml',
              'mock',
              'plone.app.customerize',
              'plone.app.robotframework',
              'plone.app.testing [robot]',
              'plone.browserlayer',
              'plone.namedfile',
              'plone.testing',
              'robotsuite',
              'six',
              'z3c.relationfield',
              'zope.intid',
              'zope.viewlet',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
