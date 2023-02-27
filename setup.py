#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name="pv211_utils",
    version='1.1.6',
    description="Utilities for PV211 project",
    long_description="",
    classifiers=[],
    author="Michal Stefanik",
    author_email="stefanik.m@fi.muni.cz",
    url="https://gitlab.fi.muni.cz",
    license="MIT",
    packages=["pv211_utils", "pv211_utils.trec", "pv211_utils.cranfield", "pv211_utils.arqmath", "pv211_utils.systems"],
    package_dir={"pv211_utils": "pv211_utils"},
    include_package_data=True,
    zip_safe=True,
    setup_requires=[
        "setuptools",
    ],
    install_requires=[
        "gspread",
        "oauth2client",
        "google",
        "tqdm",
        "ijson",
        "ipython",
        "gensim",
        "sentence_transformers",
        "torch",
        "scikit-learn"
    ],
    extras_require={
        "notebooks": [
            "gensim==3.6.0",
            "jupyterhub",
            "jupyterlab",
        ],
        "google_drive": [
            "gdown",
        ],
    },
    package_data={
        "pv211_utils": [
            "data/*",
        ],
    },
)

# vim: set cin et ts=4 sw=4 ft=python :11
