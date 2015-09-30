# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '2.0a1'
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
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
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
      author='Héctor Velarde',
      author_email='hector.velarde@gmail.com',
      url='https://github.com/collective/collective.nitf',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'AccessControl',
          'Acquisition',
          'collective.js.cycle2 >=1.0b1',
          'collective.js.jqueryui',
          'collective.prettydate >=1.1',
          'plone.api',
          'plone.app.contentmenu',
          'plone.app.dexterity [relations]',
          'plone.app.imaging',
          'plone.app.layout >=2.3.12',
          'plone.app.lockingbehavior',
          'plone.app.portlets',
          'plone.app.querystring >=1.2.5',
          'plone.app.referenceablebehavior',
          'plone.app.registry',
          'plone.app.relationfield',
          'plone.app.textfield',
          'plone.app.upgrade',
          'plone.app.vocabularies',
          'plone.behavior',
          'plone.dexterity',
          'plone.directives.form',
          'plone.formwidget.autocomplete',
          'plone.formwidget.contenttree',
          'plone.indexer',
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
          'zope.formlib',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'collective.cover',
              'mock',
              'plone.app.customerize',
              'plone.app.robotframework',
              'plone.app.testing [robot] >=4.2.2',
              'plone.browserlayer',
              'plone.namedfile',
              'plone.testing',
              'robotsuite',
              'z3c.relationfield',
              'zope.intid',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
