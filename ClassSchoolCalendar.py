#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#
# NEED : iCalendar https://pypi.python.org/pypi/icalendar
#

from __future__ import unicode_literals
from urllib import urlopen
from icalendar import Calendar, Event
from datetime import datetime 
from datetime import date 
from icalendar import LocalTimezone   
import sys, time

class schoolcalendar:
  def getschoolcalendar(self, zone):
    try:
      zoneok = str(zone.upper())
    except:
      return "Wrong Zone (must be A, B or C)"
    if len(zoneok) > 1:
      return "Wrong Zone (must be A, B or C)"
    if zoneok not in ["A","B","C"]:
      return "Wrong Zone (must be A, B or C)"
    else :
     URL = "http://media.education.gouv.fr/ics/Calendrier_Scolaire_Zone_"+zoneok+".ics"
     ics = urlopen(URL)
     cal = Calendar.from_ical(ics.read())
     datenow = datetime.now()
     year = datenow.year
     month = datenow.month
     day = datenow.day
     today = date(year,month,day)
     listvalue = []
     for event in cal.walk('vevent'):

        start = event.get('dtstart')
        convertstart = start.to_ical()
        stringconvertstart= str(convertstart)
        startdecode = time.strptime(str(convertstart), '%Y%m%d')
        end =  event.get('dtend')
        summary = event.get('summary')
        yearstart = startdecode[0]
        monthstart = startdecode[1]
        daystart = startdecode[2]
        d2 = date(yearstart, monthstart, daystart)
        description = summary.to_ical().decode('utf-8')
        if end:
           convertend = end.to_ical()
           enddecode = time.strptime(str(convertend), '%Y%m%d')
           stringconvertend= str(convertend)
           yearend = enddecode[0]
           monthend = enddecode[1]
           dayend = enddecode[2]
           listvalue.append([stringconvertstart, description,stringconvertend]) 
        else:
           listvalue.append([stringconvertstart, description]) 
     return str(listvalue)

  def isschoolcalendar(self,zone,day,month,year):
    try:
      zoneok = str(zone.upper())
    except:
      return "Wrong Zone (must be A, B or C)"
    if len(zoneok) > 1:
      return "Wrong Zone (must be A, B or C)"
    if zoneok not in ["A","B","C"]:
      return "Wrong Zone (must be A, B or C)"
    else :
     URL = "http://media.education.gouv.fr/ics/Calendrier_Scolaire_Zone_"+zoneok+".ics"
     ics = urlopen(URL)
     cal = Calendar.from_ical(ics.read())
     #datenow = datetime.now()
     #year = datenow.year
     #month = datenow.month
     #month = 9
     #day = datenow.day
     #day = 26
     today = date(year,month,day)
     startspring = u"Vacances d'\xe9t\xe9"
     endspring = u"Rentr\xe9e scolaire des \xe9l\xe8ves"
     springd2 = None
     springd3 = None

     for event in cal.walk('vevent'):
        start = event.get('dtstart')
        convertstart = start.to_ical()
        stringconvertstart= str(convertstart)
        startdecode = time.strptime(str(convertstart), '%Y%m%d')
        end =  event.get('dtend')
        summary = event.get('summary')
        yearstart = startdecode[0]
        monthstart = startdecode[1]
        daystart = startdecode[2]
        d2 = date(yearstart, monthstart, daystart)
        d3 = None
        description = summary.to_ical().decode('utf-8')
        if str(year) in convertstart:
          if  startspring in summary :
              if d2 is not None :
                springd2 = d2
          if endspring in summary:
              if d2 is not None:
                springd3 = d2
          comparestart = ""
          compareend = ""
          if springd2:
            comparestart = springd2 < today
          if springd3:
            compareend = today < springd3
          if comparestart and compareend:
            description = startspring.encode('utf-8')
            return str(description)
              
        if end:
           convertend = end.to_ical()
           enddecode = time.strptime(str(convertend), '%Y%m%d')
           stringconvertend= str(convertend)
           yearend = enddecode[0]
           monthend = enddecode[1]
           dayend = enddecode[2]
           d3 = date(yearend, monthend, dayend)
           if d2 < today < d3:
             return description
           else:
             pass
