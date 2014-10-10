#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

# NEED http://www.crummy.com/software/BeautifulSoup/

# EDF website url
#https://particuliers.edf.com/gestion-de-mon-contrat/options-tarifaires/option-ejp/l-observatoire-2584.html

import urllib
from urllib2 import urlopen
import sys
import bs4 as BeautifulSoup

class EDFejp:
  def __init__(self):
    self.ejpoui = "/FRONT/NetExpress/img/ejp_oui.png"
    self.ejpnon = "/FRONT/NetExpress/img/ejp_non.png"
    self.ejpnd = "/FRONT/NetExpress/img/ejp_nd.png"


  def EJPToday(self,request):
    try:
      html = urlopen('https://particuliers.edf.com/gestion-de-mon-contrat/options-tarifaires/option-ejp/l-observatoire-2584.html').read()
      soup = BeautifulSoup.BeautifulSoup(html)
    except:
      return None

    dumptoday = soup.findAll('table', attrs={"class":u"w_skinnedTable reacapEJPDay"})[1]
    for x in dumptoday :
      if request == "nord" :
        result= soup.find('td', attrs={"headers":u"tabEJP1_1-h2 tabEJP1_1-l1"})
      if request == "sud":
        result = soup.find('td', attrs={"headers":u"tabEJP1_1-h5 tabEJP1_1-l1"})
      if request == "ouest":
        result = soup.find('td', attrs={"headers":u"tabEJP1_1-h4 tabEJP1_1-l1"})
      if request == "paca":
        result = soup.find('td', attrs={"headers":u"tabEJP1_1-h3 tabEJP1_1-l1"})
      if self.ejpoui in str(result):
        return "True"
      elif self.ejpnon in str(result):
        return "False"
      elif self.ejpnd in str(result):
        return "ND"
      else:
        return "no data"
      break

  def EJPTomorrow(self,request):
    try:
      html = urlopen('https://particuliers.edf.com/gestion-de-mon-contrat/options-tarifaires/option-ejp/l-observatoire-2584.html').read()
      soup = BeautifulSoup.BeautifulSoup(html)
    except:
      return None

    dumptoday = soup.findAll('table', attrs={"class":u"w_skinnedTable reacapEJPDay"})[0]
    for x in dumptoday :
      if request == "nord" :
        result= soup.find('td', attrs={"headers":u"tabEJP2_1-h2 tabEJP2_1-l1"})
      if request == "sud":
        result = soup.find('td', attrs={"headers":u"tabEJP2_1-h5 tabEJP2_1-l1"})
      if request == "ouest":
        result = soup.find('td', attrs={"headers":u"tabEJP2_1-h4 tabEJP2_1-l1"})
      if request == "paca":
        result = soup.find('td', attrs={"headers":u"tabEJP2_1-h3 tabEJP2_1-l1"})
      if self.ejpoui in str(result):
        return "True"
      elif self.ejpnon in str(result):
        return "False"
      elif self.ejpnd in str(result):
        return "ND"
      else:
        return "no data"
      break
