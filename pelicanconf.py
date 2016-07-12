#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import datetime

AUTHOR = u'Noah Hoffman'
SITENAME = u'borborygmi'
SITEURL = 'http://nhoffman.github.io/borborygmi'
COPYRIGHT_YEAR = datetime.date.today().year

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Faculty Site', 'http://web.labmed.washington.edu/nhoffman'),
         ('UW Lab Medicine', 'http://depts.washington.edu/labweb/'),
         ('my GitHub', 'https://github.com/nhoffman'),
         ('site source', 'https://github.com/nhoffman/borborygmi'),)

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

GOOGLE_ANALYTICS = "UA-16886766-2"
