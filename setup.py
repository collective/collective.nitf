# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.nitf',
      version=version,
      description="A Dexterity-based content type inspired on the News Industry Text Format specification.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone dexterity nitf',
      author='Héctor Velarde',
      author_email='hector.velarde@gmail.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.dexterity',
          'plone.app.transmogrifier',
          'transmogrify.dexterity',
          'collective.autopermission',
          'collective.testcaselayer',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
