# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0a4.dev0'
description = "A content type inspired on the IPTC's News Industry Text \
Format specification."
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.nitf',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
#        "Framework :: Plone :: 4.3",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dexterity iptc newsml nitf',
      author='Héctor Velarde',
      author_email='hector.velarde@gmail.com',
      url='https://github.com/collective/collective.nitf',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'beautifulsoup4',
        'Pillow',
        'Products.CMFPlone>=4.2',
        'collective.js.jqueryui',
        'collective.prettydate>=1.1',
        'collective.z3cform.widgets',
        'plone.app.dexterity[grok]',
        'plone.app.lockingbehavior',
        'plone.app.referenceablebehavior',
        ],
      extras_require={
        'test': [
          'plone.app.testing',
          'robotsuite',
          'robotframework-selenium2library',
          ],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
