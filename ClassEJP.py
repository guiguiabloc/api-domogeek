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

url="https://particulier.edf.fr/bin/edf_rc/servlets/ejptempo?searchType=ejp"

class EDFejp:

  def EJPToday(self,request):
    print "RECU REQUETE: " +request
    try:
      html = urllib2.urlopen(url)
    except:
      return None
    try:
      rep = json.load(html)
    except:
      return None
    data = rep["data"]
    try:
      d = json.loads(data)
    except:
      return None
    info_ejp=d['dtos']
    result = None
    lst = []
    for i in info_ejp:
      d=i['dates'][0]
      v=i['values'][0]
      r=i['region']
      liste = {}
      liste[r]=v
      lst.append(liste)
    resultat = json.dumps(lst)
    NORD = lst[0]['EJP_NORD']
    OUEST = lst[1]['EJP_OUEST']
    PACA = lst[2]['EJP_PACA']
    SUD = lst[3]['EJP_SUD']
    print NORD, OUEST, PACA, SUD
    if request == "nord":
        result= NORD
    if request == "sud":
        result = SUD
    if request == "ouest":
        result = OUEST
    if request == "paca":
        result = PACA
    print result
    if "OUI" in str(result):
        return "True"
    elif "NON" in str(result):
        return "False"
    elif "ND" in str(result):
        return "ND"
    else:
        return "no data"

  def EJPTomorrow(self,request):
    print "RECU REQUETE: " +request
    try:
      html = urllib2.urlopen(url)
    except:
      return None
    try:
      rep = json.load(html)
    except:
      return None
    data = rep["data"]
    try:
      d = json.loads(data)
    except:
      return None
    info_ejp=d['dtos']
    result = None
    lst = []
    for i in info_ejp:
      try:
        d_tomorrow=i['dates'][1]
        v_tomorrow=i['values'][1]
        r=i['region']
        liste = {}
        liste[r]=v
        lst.append(liste)
        resultat = json.dumps(lst)
      except:
        return "no value"
    NORD = lst[0]['EJP_NORD']
    OUEST = lst[1]['EJP_OUEST']
    PACA = lst[2]['EJP_PACA']
    SUD = lst[3]['EJP_SUD']
    print NORD, OUEST, PACA, SUD
    if request == "nord":
        result= NORD
    if request == "sud":
        result = SUD
    if request == "ouest":
        result = OUEST
    if request == "paca":
        result = PACA
    print result
    if "OUI" in str(result):
        return "True"
    elif "NON" in str(result):
        return "False"
    elif "ND" in str(result):
        return "ND"
    else:
        return "no data"

