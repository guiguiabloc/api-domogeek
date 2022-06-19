#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

import urllib3
import sys
import json
import datetime
from datetime import timedelta

class EDFTempo:
  def TempoToday(self):
    now = datetime.datetime.now()
    today= now.strftime("%Y-%m-%d")
    try:
      page = urllib3.urlopen('https://particulier.edf.fr/bin/edf_rc/servlets/ejptemponew?Date_a_remonter='+today+'&TypeAlerte=TEMPO')
    except:
      return None
    response = json.load(page)
    colortoday = response['JourJ']['Tempo']
    return colortoday

  def TempoTomorrow(self):
    now = datetime.datetime.now()
    datetomorrow = now + timedelta(days=1)
    tomorrow = datetomorrow.strftime("%Y-%m-%d")
    try:
      page = urllib3.urlopen('https://particulier.edf.fr/bin/edf_rc/servlets/ejptemponew?Date_a_remonter='+tomorrow+'&TypeAlerte=TEMPO')
    except:
      return None
    response = json.load(page)
    try:
      colortomorrow = response['JourJ']['Tempo']
      return colortomorrow
    except:
      return "no color"

