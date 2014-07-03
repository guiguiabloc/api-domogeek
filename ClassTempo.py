#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

# NEED http://www.crummy.com/software/BeautifulSoup/

# EDF website url
#https://particuliers.edf.com/gestion-de-mon-contrat/options-tarifaires/la-couleur-du-jour-2585.html

import urllib
from urllib2 import urlopen
import sys
import bs4 as BeautifulSoup

class EDFTempo:
  def __init__(self):
    self.tempobleu = '<li class="blue">X</li>'
    self.tempoblanc = '<li class="white">X</li>'
    self.temporouge = '<li class="red">X</li>'

  def TempoToday(self):
    try:
      html = urlopen('https://particuliers.edf.com/gestion-de-mon-contrat/options-tarifaires/la-couleur-du-jour-2585.html').read()
      soup = BeautifulSoup.BeautifulSoup(html)
    except:
      return None
    dumptoday = soup.findAll('div', attrs={"class":u"tempoInfos"})[0]
    dumptomorrow = soup.findAll('div', attrs={"class":u"tempoInfos"})[1]
    self.tempotoday = str(dumptoday)
    self.tempotomorrow = str(dumptomorrow)
    if self.tempobleu in self.tempotoday:
      return "bleu"
    if self.tempoblanc in self.tempotoday:
      return "blanc"
    if self.temporouge in self.tempotoday:
      return "rouge"

  def TempoTomorrow(self):
    try:
      html = urlopen('https://particuliers.edf.com/gestion-de-mon-contrat/options-tarifaires/la-couleur-du-jour-2585.html').read()
      soup = BeautifulSoup.BeautifulSoup(html)
    except:
      return None
    dumptoday = soup.findAll('div', attrs={"class":u"tempoInfos"})[0]
    dumptomorrow = soup.findAll('div', attrs={"class":u"tempoInfos"})[1]
    self.tempotoday = str(dumptoday)
    self.tempotomorrow = str(dumptomorrow)

    if self.tempobleu in self.tempotomorrow:
      return "bleu"
    if self.tempoblanc in self.tempotomorrow:
      return "blanc"
    if self.temporouge in self.tempotomorrow:
      return "rouge"


