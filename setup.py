# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

version = '1.0dev'
long_description = "%s\n%s\n%s\n%s" % (
                        open("README.rst").read(),
                        open(os.path.join("docs", "INSTALL.txt")).read(),
                        open(os.path.join("docs", "CREDITS.txt")).read(),
                        open(os.path.join("docs", "HISTORY.txt")).read(),
                        )

setup(name='collective.nitf',
      version=version,
      description="A Dexterity-based content type inspired on the News Industry Text Format specification.",
      long_description=long_description,
      classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dexterity nitf',
      author='Héctor Velarde',
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
        'collective.js.jqueryui',
        'plone.app.dexterity>=1.1',
        'plone.app.referenceablebehavior',
        'plone.app.lockingbehavior',
        'plone.app.relationfield',
        'collective.prettydate'
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
