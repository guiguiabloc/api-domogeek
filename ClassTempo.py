#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

import urllib2
import sys
import json

class EDFTempo:
  def TempoToday(self):
    try:
      page = urllib2.urlopen('https://particulier.edf.fr/bin/edf_rc/servlets/ejptempo?searchType=tempo')
    except:
      return None
    response = json.load(page)
    data=response["data"]
    colortoday = data.split('"')[9]
    return colortoday

  def TempoTomorrow(self):
    try:
      page = urllib2.urlopen('https://particulier.edf.fr/bin/edf_rc/servlets/ejptempo?searchType=tempo')
    except:
      return None
    response = json.load(page)
    data=response["data"]
    try:
      colortomorrow = data.split('"')[17]
      return colortomorrow
    except:
      return "no color"


