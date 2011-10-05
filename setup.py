# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0dev'

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
      author='Héctor Velarde, Joaquín Rosales',
      author_email='hector.velarde@gmail.com',
      url='https://github.com/collective/collective.nitf',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'collective.transmogrifier',
        'plone.app.dexterity>=1.0.3',
        'plone.app.transmogrifier',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
