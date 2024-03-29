# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = "3.0.0.dev0"
description = (
    "A content type inspired on the IPTC's News Industry Text Format specification."
)
long_description = (
    open("README.rst").read()
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
)

setup(
    name="collective.nitf",
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone dexterity iptc newsml nitf",
    author="Hector Velarde",
    author_email="hector.velarde@gmail.com",
    url="https://github.com/collective/collective.nitf",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    python_requires="~=2.7, ~=3.7, ~=3.8",
    install_requires=[
        "Acquisition",
        "plone.api",
        "plone.app.content",
        "plone.app.dexterity [relations]",
        "plone.app.layout",
        "plone.app.lockingbehavior",
        "plone.app.registry",
        "plone.app.relationfield",
        "plone.app.textfield",
        "plone.app.vocabularies",
        "plone.autoform",
        "plone.behavior",
        "plone.dexterity",
        "plone.indexer",
        "plone.memoize",
        "plone.namedfile",
        "plone.registry",
        "plone.resource",
        "plone.supermodel",
        "plone.uuid",
        "Products.CMFPlone >=5.2",
        "Products.GenericSetup",
        "setuptools",
        "zope.browserpage",
        "zope.component",
        "zope.deprecation",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
    ],
    extras_require={
        "test": [
            "AccessControl",
            "lxml",
            "mock",
            "plone.app.customerize",
            "plone.app.robotframework",
            "plone.app.testing [robot]",
            "plone.browserlayer",
            "plone.namedfile",
            "plone.testing",
            "Products.CMFCore",
            "robotsuite",
            "six",
            "z3c.relationfield",
            "zope.intid",
            "zope.viewlet",
        ],
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
