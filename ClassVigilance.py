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
    if len(deprequest) != 2:
      return "Error in department number"
    url = 'http://vigilance.meteofrance.com/data/NXFR34_LFPW_.xml'
    dom = minidom.parse(urllib.urlopen(url))
    parsexml = dom.getElementsByTagName('datavigilance')
    def color(number):
      if number == "1":
       return "vert"
      if number == "2":
       return "jaune"
      if number == "3":
       return "rouge"
    for all in parsexml :
      depart = all.attributes['dep'].value
      colorresult = all.attributes['couleur'].value
      if depart == deprequest: 
        result = color(colorresult)
        return result
