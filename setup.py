#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages
    
import os

setup(
    name = "django-irs",
    version = "0.1",
    url = 'http://www.synchrosinteractive.com/projects',
	download_url = 'http://github.com/dmcquay/django-irs/downloads',
    license = 'Creative Commons Attribution-Share Alike 3.0 United States License',
    description = "An image rendering service for Django.",
    author = 'Dustin McQuay',
    author_email = 'dmcquay@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
