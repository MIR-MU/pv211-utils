#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import find_packages, setup

setup(
    name="pv211_utils",
    version='0.2',
    description="Utilities for PV211 project",
    long_description="",
    classifiers=[],
    author="Michal Stefanik",
    author_email="stefanik.m@fi.muni.cz",
    url="https://gitlab.fi.muni.cz",
    license="MIT",
    packages=["pv211_utils"],
    package_dir={"pv211_utils": "pv211_utils"},
    use_scm_version={"write_to": ".version", "write_to_template": "{version}\n"},
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        "setuptools",
        "gspread",
        "oauth2client",
        "google",
    ],
    package_data={"pv211_utils": ["data/*"]},
)

# vim: set cin et ts=4 sw=4 ft=python :11
