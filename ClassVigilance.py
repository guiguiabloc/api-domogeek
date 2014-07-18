#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

import urllib
from xml.dom import minidom


class vigilance:
  def getvigilance(self, deprequest):
    print deprequest
    if len(deprequest) != 2:
      return "Error in department number"
    url = 'http://vigilance.meteofrance.com/data/NXFR34_LFPW_.xml'
    dom = minidom.parse(urllib.urlopen(url))
    def color(number):
      if number == "0":
       return "vert"
      if number == "1":
       return "vert"
      if number == "2":
       return "jaune"
      if number == "3":
       return "orange"
      if number == "4":
       return "rouge"
    def risklong(number):
      if number == "1":
       return "vent"
      if number == "2":
       return "pluie-inondation"
      if number == "3":
       return "orages"
      if number == "4":
       return "inondations"
      if number == "5":
       return "neige-verglas"
      if number == "6":
       return "canicule"
      if number == "7":
       return "grand-froid"

    for all in dom.getElementsByTagName('datavigilance'):
         depart = all.attributes['dep'].value
         colorresult = all.attributes['couleur'].value
         riskresult = "RAS"
         for risk in all.getElementsByTagName('risque'):
              riskresult = risk.attributes['valeur'].value
         for flood in all.getElementsByTagName('crue'):
              floodresult = flood.attributes['valeur'].value
         riskresult = risklong(riskresult)
         floodresult = color(floodresult)
         if not riskresult: 
           riskresult = "RAS"
         if depart == deprequest:
           color = color(colorresult)
           return color, riskresult, floodresult

