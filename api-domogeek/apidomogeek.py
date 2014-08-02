#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

import sys
import json
import hashlib
import time
from datetime import datetime,date,timedelta
import urllib2

import web
from Daemon import Daemon
import Holiday
import ClassTempo
import ClassSchoolCalendar
import ClassVigilance
import ClassGeoLocation
import ClassDawnDusk
import ClassWeather


school = ClassSchoolCalendar.schoolcalendar()
dayrequest = Holiday.jourferie()
temporequest = ClassTempo.EDFTempo()
vigilancerequest = ClassVigilance.vigilance()
geolocationrequest = ClassGeoLocation.geolocation()
dawnduskrequest = ClassDawnDusk.sunriseClass()
weatherrequest = ClassWeather.weather()

##########
# CONFIG #
##########

listenip = "0.0.0.0"
listenport = "80"
localapiurl= "http://api.domogeek.fr"
googleapikey = ''
bingmapapikey = ''
geonameskey = ''

redis_host =  "127.0.0.1"
redis_port =  6379

##############
# END CONFIG #
##############

##############
# Test REDIS #
##############
try:
 import redis
except:
  print "No Redis module : https://pypi.python.org/pypi/redis/"
  sys.exit(1)


web.config.debug = False


urls = (
  '/holiday/(.*)', 'holiday',
  '/tempoedf/(.*)', 'tempoedf',
  '/schoolholiday/(.*)', 'schoolholiday',
  '/weekend/(.*)', 'weekend',
  '/holidayall/(.*)', 'holidayall',
  '/vigilance/(.*)', 'vigilance',
  '/geolocation/(.*)', 'geolocation',
  '/sun/(.*)', 'dawndusk',
  '/weather/(.*)', 'weather',
  '/', 'index'
)

app = web.application(urls, globals())

class index:
    def GET(self):
        # redirect to the static file ...
        raise web.seeother('/static/index.html')


"""
@api {get} /holiday/:date/:responsetype Holiday Status Request
@apiName GetHoliday
@apiGroup Domogeek
@apiDescription Ask to know if :date is a holiday
@apiParam {String} now  Ask for today.
@apiParam {String} all  Ask for all entry.
@apiParam {Datetime} D-M-YYYY  Ask for specific date.
@apiParam {String} [responsetype]  Specify Response Type (raw by default or specify json, only for single element).
@apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     Jour de Noel

     HTTP/1.1 200 OK
     no

@apiErrorExample Error-Response:
     HTTP/1.1 400 Bad Request
     400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/holiday/now
     curl http://api.domogeek.fr/holiday/now/json
     curl http://api.domogeek.fr/holiday/all
     curl http://api.domogeek.fr/holiday/25-12-2014/json

"""

class holiday:
    def GET(self,uri):
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /holiday/{now / date(D-M-YYYY)}\n"
      try:
        format = request[1]
      except:
        format = None
      if request[0] == "now":
        datenow = datetime.now()
        year = datenow.year
        month = datenow.month
        day = datenow.day 
        result = dayrequest.estferie([day,month,year])
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"holiday": result})
        else:
          return result
      if request[0] == "all":
        datenow = datetime.now()
        year = datenow.year
        listvalue = []
        F, J, L = dayrequest.joursferies(year,1,'/')
        for i in xrange(0,len(F)):
          result = F[i], "%10s" % (J[i]), L[i]
          listvalue.append(result)
          response = json.dumps(listvalue)
        return response

      if request[0] != "now" and request[0] != "all":
        try:
          daterequest = request[0]
          result = daterequest.split('-') 
        except:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        try:
          day = int(result[0])
          month = int(result[1])
          year = int(result[2])
        except:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        if day > 31 or month > 12:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        result = dayrequest.estferie([day,month,year])
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"holiday": result})
        else:
          return result


"""
@api {get} /weekend/:daterequest/:responsetype Week-end Status Request
@apiName GetWeekend
@apiGroup Domogeek
@apiDescription Ask to know if :daterequest is a week-end day
@apiParam {String} daterequest Ask for specific date {now | tomorrow | D-M-YYYY}.
@apiParam {String} [responsetype]  Specify Response Type (raw by default or specify json, only for single element).
@apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     True

     HTTP/1.1 200 OK
     False

@apiErrorExample Error-Response:
     HTTP/1.1 400 Bad Request
     400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/weekend/now
     curl http://api.domogeek.fr/weekend/tomorrow
     curl http://api.domogeek.fr/weekend/now/json
     curl http://api.domogeek.fr/weekend/16-07-2014/json

"""
class weekend:
    def GET(self,uri):
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /weekend/{now|tomorrow|date(D-M-YYYY)}\n"
      try:
        format = request[1]
      except:
        format = None
      if request[0] == "now":
        datenow = datetime.now()
        daynow = datetime.now().weekday()
        day = datenow.day
        if daynow == 5 or daynow == 6:
          result = "True"
        else:
          result = "False"
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"weekend": result})
        else:
          return result
      if request[0] == "tomorrow":
        today = date.today()
        datetomorrow = today + timedelta(days=1)
        day = datetomorrow.weekday()
        if day == 5 or day == 6:
          result = "True"
        else:
          result = "False"
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"weekend": result})
        else:
          return result
      if request[0] != "now" and request[0] != "tomorrow":
        try:
          daterequest = request[0]
          day,month,year = daterequest.split('-')
        except:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        try:
          int(day)
          int(month)
          int(year)
        except:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        requestday = date(int(year),int(month),int(day)).weekday()
        if requestday == 5 or requestday == 6:
          result = "True"
        else:
          result = "False"
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"weekend": result})
        else:
          return result

"""
@api {get} /holidayall/:zone/:daterequest All Holidays Status Request
@apiName GetHolidayall
@apiGroup Domogeek
@apiDescription Ask to know if :daterequest is a holiday, school holiday and week-end day
@apiParam {String} zone  School Zone (A, B or C).
@apiParam {String} daterequest Ask for specific date {now | D-M-YYYY}.
@apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {"holiday": "False", "weekend": "False", "schoolholiday": "Vacances de printemps - Zone A"}


@apiErrorExample Error-Response:
     HTTP/1.1 400 Bad Request
     400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/holidayall/A/now
     curl http://api.domogeek.fr/holidayall/B/25-02-2014
"""
class holidayall:
    def GET(self,uri):
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /holidayall/{zone}/{now|date(D-M-YYYY)}\n"
      try:
        zone = request[0]
      except:
        return "Incorrect request : /holidayall/{zone}/{now|date(D-M-YYYY)}\n"
      try:
        zoneok = str(zone.upper())
      except:
        return "Wrong Zone (must be A, B or C)"
      if len(zoneok) > 1:
        return "Wrong Zone (must be A, B or C)"
      if zoneok not in ["A","B","C"]:
        return "Incorrect request : /holidayall/{zone}/{now|date(D-M-YYYY)}\n"
      try:
        daterequest = request[1]
      except:
        return "Incorrect request : /holidayall/{zone}/{now|date(D-M-YYYY)}\n"
      if request[1] == "now":
        responseholiday = urllib2.urlopen(localapiurl+'/holiday/now')
        responseschoolholiday = urllib2.urlopen(localapiurl+'/schoolholiday/'+zoneok+'/now')
        responseweekend = urllib2.urlopen(localapiurl+'/weekend/now')
        resultholiday = responseholiday.read()
        resultschoolholiday = responseschoolholiday.read()
        resultschoolholidays = resultschoolholiday.decode('utf-8')
        resultweekend = responseweekend.read()
        web.header('Content-Type', 'application/json')
        return json.dumps({"holiday": resultholiday, "schoolholiday": resultschoolholidays, "weekend": resultweekend}, ensure_ascii=False).encode('utf8')
      if request[1] != "now":
        try:
          daterequest = request[1]
          day,month,year = daterequest.split('-')
        except:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        try:
          int(day)
          int(month)
          int(year)
        except:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        responseholiday = urllib2.urlopen(localapiurl+'/holiday/'+daterequest)
        responseschoolholiday = urllib2.urlopen(localapiurl+'/schoolholiday/'+zoneok+'/'+daterequest)
        responseweekend = urllib2.urlopen(localapiurl+'/weekend/'+daterequest)
        resultholiday = responseholiday.read()
        resultschoolholiday = responseschoolholiday.read()
        resultschoolholidays = resultschoolholiday.decode('utf-8')
        resultweekend = responseweekend.read()
        web.header('Content-Type', 'application/json')
        return json.dumps({"holiday": resultholiday, "schoolholiday": resultschoolholidays, "weekend": resultweekend}, ensure_ascii=False).encode('utf8')


"""
@api {get} /tempoedf/:date/:responsetype Tempo EDF color Request
@apiName GetTempo
@apiGroup Domogeek
@apiDescription Ask the EDF Tempo color
@apiParam {String} now  Ask for today.
@apiParam {String} tomorrow Ask for tomorrow.
@apiParam {String} [responsetype]  Specify Response Type (raw by default or specify json, only for single element).
@apiSuccessExample Success-Response:
HTTP/1.1 200 OK
Content-Type: application/json
Transfer-Encoding: chunked
Date: Thu, 03 Jul 2014 17:16:47 GMT
Server: localhost
{"tempocolor": "bleu"}

@apiErrorExample Error-Response:
HTTP/1.1 400 Bad Request
400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/tempoedf/now
     curl http://api.domogeek.fr/tempoedf/now/json
     curl http://api.domogeek.fr/tempoedf/tomorrow
     curl http://api.domogeek.fr/tempoedf/tomorrow/json

"""

class tempoedf:
    def GET(self,uri):
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /tempoedf/{now | tomorrow}\n"
      try:
        format = request[1]
      except:
        format = None
      if request[0] == "now":
        result = temporequest.TempoToday()
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"tempocolor": result})
        else:
          return result
      if request[0] == "tomorrow":
        result = temporequest.TempoTomorrow()
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"tempocolor": result})
        else:
          return result
      web.badrequest()
      return "Incorrect request : /tempoedf/{now | tomorrow}\n"


"""
@api {get} /schoolholiday/:zone/:daterequest/:responsetype School Holiday Status Request
@apiName GetSchoolHoliday
@apiGroup Domogeek
@apiDescription Ask to know if :daterequest is a school holiday (UTF-8 response)
@apiParam {String} zone  School Zone (A, B or C).
@apiParam {String} daterequest Ask for specific date {now | all | D-M-YYYY}.
@apiParam {String} [responsetype]  Specify Response Type (raw by default or specify json, only for single element).
@apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     Vacances de la Toussaint 

     HTTP/1.1 200 OK
     False

@apiErrorExample Error-Response:
     HTTP/1.1 400 Bad Request
     400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/schoolholiday/A/now
     curl http://api.domogeek.fr/schoolholiday/A/now/json
     curl http://api.domogeek.fr/schoolholiday/A/all
     curl http://api.domogeek.fr/schoolholiday/A/25-12-2014/json

"""

class schoolholiday:
    def GET(self,uri):
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /schoolholiday/{zone}/{now/all/date(D-M-YYYY)}\n"
      try:
        zone = request[0]
      except:
        return "Incorrect request : /schoolholiday/{zone}/{now/all/date(D-M-YYYY)}\n"
      try:
        zoneok = str(zone.upper())
      except:
        return "Wrong Zone (must be A, B or C)"
      if len(zoneok) > 1:
        return "Wrong Zone (must be A, B or C)"

      if zoneok not in ["A","B","C"]:
        return "Incorrect request : /schoolholiday/{zone}/{now/all/date(D-M-YYYY)}\n"
      try:
        daterequest = request[1]
      except:
        return "Incorrect request : /schoolholiday/{zone}/{now/all/date(D-M-YYYY)}\n"
      try:
        format = request[2]
      except:
        format = None
      datenow = datetime.now()
      year = datenow.year
      month = datenow.month
      day = datenow.day

      if daterequest == "now":
        result = school.isschoolcalendar(zoneok,day,month,year)
        if result == None :
          result = "False"
        try:
          description = result.decode('utf-8')
        except:
          description = result
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"schoolholiday": description}, ensure_ascii=False).encode('utf8')
        else:
          return description
      if daterequest == "all":
        result = school.getschoolcalendar(zone)
        try:
          description = result.decode('unicode_escape')
        except:
          description = result
        web.header('Content-Type', 'application/json')
        return description
      if daterequest != "now" and daterequest != "all":
        try:
          result = daterequest.split('-')
        except:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        try:
          day = int(result[0])
          month = int(result[1])
          year = int(result[2])
        except:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        if day > 31 or month > 12:
          web.badrequest()
          return "Incorrect date format : D-M-YYYY\n"
        result = school.isschoolcalendar(zoneok,day,month,year)
        if result == None :
          result = "False"
        try:
          description = result.decode('utf-8')
        except:
          description = result
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"schoolholiday": description}, ensure_ascii=False).encode('utf8')
        else:
          return description


"""
@api {get} /vigilance/:department/:vigilancerequest/:responsetype Vigilance MeteoFrance 
@apiName GetVigilance
@apiGroup Domogeek
@apiDescription Ask Vigilance MeteoFrance for :department
@apiParam {String} department Department number (France Metropolitan).
@apiParam {String} vigilancerequest Vigilance request {color|risk|flood|all}.
@apiParam {String} [responsetype]  Specify Response Type (raw by default or specify json, only for single element).
@apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {"vigilanceflood": "jaune", "vigilancecolor": "orange", "vigilancerisk": "orages"}

     HTTP/1.1 200 OK
     vert 

@apiErrorExample Error-Response:
     HTTP/1.1 400 Bad Request
     400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/vigilance/29/color
     curl http://api.domogeek.fr/vigilance/29/color/json
     curl http://api.domogeek.fr/vigilance/29/risk/json
     curl http://api.domogeek.fr/vigilance/29/all

"""
class vigilance:
    def GET(self,uri):
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /vigilance/{department}/{color|risk|flood|all}\n"
      try:
        dep = request[0]
      except:
        return "Incorrect request : /vigilance/{department}/{color|risk|flood|all}\n"
      try:
        vigilancequery = request[1]
      except:
        return "Incorrect request : /vigilance/{department}/{color|risk|flood|all}\n"
      try:
        format = request[2]
      except:
        format = None
      if vigilancequery not in ["color","risk","flood", "all"]: 
        return "Incorrect request : /vigilance/{department}/{color|risk|flood|all}\n"
      result = vigilancerequest.getvigilance(dep)
      color =  result[0]
      risk =  result[1]
      flood =  result[2]
      if vigilancequery == "color":
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"vigilancecolor": color})
        else:
          return color
      if vigilancequery == "risk":
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"vigilancerisk": risk})
        else:
          return risk
      if vigilancequery == "flood":
        if format == "json":
          web.header('Content-Type', 'application/json')
          return json.dumps({"vigilanceflood": flood})
        else:
          return flood
      if vigilancequery == "all":
        web.header('Content-Type', 'application/json')
        return json.dumps({"vigilancecolor": color, "vigilancerisk": risk, "vigilanceflood": flood})




"""
@api {get} /geolocation/:city City Geolocation 
@apiName GetGeolocation
@apiGroup Domogeek
@apiDescription Ask geolocation (latitude/longitude) :city
@apiParam {String} city City name (avoid accents, no space, no guarantee works other than France Metropolitan).
@apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {"latitude": 48.390394000000001, "longitude": -4.4860759999999997}

@apiErrorExample Error-Response:
     HTTP/1.1 400 Bad Request
     400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/geolocation/brest
"""
class geolocation:
    def GET(self,uri):
      checkgoogle = False
      checkbing = False
      checkgeonames = False
      inredis = False
      request = uri.split('/')

      # Check if redis running
      rc= redis.Redis(host=redis_host, port=redis_port)
      rc.set("test", "ok")
      rc.expire("test" ,10)
      value = rc.get("test")
      if value is None:
        web.badrequest()
        return "Could not connect to  Redis  " + redis_host + " port " + redis_port

      if request == ['']:
        web.badrequest()
        return "Incorrect request : /geolocation/{city}\n"
      try:
        city = request[0]
      except:
        return "Incorrect request : /geolocation/{city}\n"
      try:
        rediskey =  hashlib.md5(city).hexdigest()
        getlocation = rc.get(rediskey)
        if getlocation is None:
          pass
        else:
          print "FOUND LOCATION IN REDIS !!!"
          inredis = "ok"
          tr1 =  getlocation.replace("(","")
          tr2 = tr1.replace(")","")
          data = tr2.split(',')
          web.header('Content-Type', 'application/json')
          return json.dumps({"latitude": float(data[0]), "longitude": float(data[1])})

      except:
        pass

      if googleapikey == '' or inredis == "ok":
        pass
      else:
        try:
          data = geolocationrequest.geogoogle(city, googleapikey)
          checkgoogle = True
          rediskey =  hashlib.md5(city).hexdigest()
          rc.set(rediskey, (data[0], data[1]))
          web.header('Content-Type', 'application/json')
          return json.dumps({"latitude": data[0], "longitude": data[1]})
        except:
          print "NO VALUE FROM GOOGLE"

      if bingmapapikey == '' or inredis == "ok":
        pass
      else:
        if checkgoogle:
          pass
        else:
          try:
            data = geolocationrequest.geobing(city, bingmapapikey)
          except:
            print "NO VALUE FROM BING"
            data = False
          if not data :
            print "NO BING"
          else:
            checkbing = True
            rediskey =  hashlib.md5(city).hexdigest()
            rc.set(rediskey, (data[0], data[1]))
            web.header('Content-Type', 'application/json')
            return json.dumps({"latitude": data[0], "longitude": data[1]})

      if geonameskey == '' or inredis == "ok":
        pass
      else:
        if checkbing:
          pass
        else:
          try:
            data = geolocationrequest.geonames(city, geonameskey)
          except:
            print "NO VALUE FROM GEONAMES"
            data = False
          if not data :
            print "NO VALUE FROM GEONAMES"
          else:
            checkgeonames = True
            rediskey =  hashlib.md5(city).hexdigest()
            rc.set(rediskey, (data[0], data[1]))
            web.header('Content-Type', 'application/json')
            return json.dumps({"latitude": data[0], "longitude": data[1]})

      if not checkgoogle and not checkbing and not checkgeonames and not inredis:
         return "NO GEOLOCATION DATA AVAILABLE\n"

"""
@api {get} /sun/:city/:sunrequest/:date/:responsetype Sun Status Request 
@apiName GetSun
@apiGroup Domogeek
@apiDescription Ask to know sunrise, sunset, zenith, day duration for :date in :city (France)
@apiParam {String} city City name (avoid accents, no space, France Metropolitan).
@apiParam {String} sunrequest  Ask for {sunrise | sunset | zenith | dayduration | all}.
@apiParam {String} date  Date request {now | tomorrow}.
@apiParam {String} [responsetype]  Specify Response Type (raw by default or specify json, only for single element).
@apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {"sunset": "20:59"}

     HTTP/1.1 200 OK
     {"dayduration": "15:06", "sunset": "21:18", "zenith": "13:44", "sunrise": "6:11"}

@apiErrorExample Error-Response:
     HTTP/1.1 400 Bad Request
     400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/sun/brest/all/now
     curl http://api.domogeek.fr/sun/bastia/sunset/now/json
     curl http://api.domogeek.fr/sun/strasbourg/sunrise/tomorrow

"""
class dawndusk:
    def GET(self,uri):
      getutc = float(time.strftime("%z")[:3])
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /sun/city/{sunrise|sunset|zenith|dayduration|all}/{now|tomorrow}\n"
      try:
        city = request[0]
      except:
        return "Incorrect request : /sun/city/{sunrise|sunset|zenith|dayduration|all}/{now|tomorrow}\n"
      try:
        dawnduskrequestelement = request[1]
      except:
        return "Incorrect request : /sun/city/{sunrise|sunset|zenith|dayduration|all}/{now|tomorrow}\n"
      try:
        daterequest = request[2]
      except:
       return "Incorrect request : /sun/city/{sunrise|sunset|zenith|dayduration|all}/{now|tomorrow}\n"
      try:
        format = request[3]
      except:
        format = None
      if dawnduskrequestelement not in ["sunrise", "sunset", "zenith", "dayduration", "all"]:
        return "Incorrect request : /sun/city/{sunrise|sunset|zenith|dayduration|all}/{now|tomorrow}\n"
      responsegeolocation = urllib2.urlopen(localapiurl+'/geolocation/'+city)
      resultgeolocation = json.load(responsegeolocation)
      try:
        latitude =  resultgeolocation["latitude"]
        longitude =  resultgeolocation["longitude"]
      except:
        return "NO GEOLOCATION DATA AVAILABLE\n"
      if request[2] == "now":
        today=date.today()
      elif request[2] == "tomorrow":
        today = date.today() + timedelta(days=1)
      else:
        return "Incorrect request : /sun/city/{sunrise|sunset|zenith|dayduration|all}/{now|tomorrow}\n"
      dawnduskrequest.setNumericalDate(today.day,today.month,today.year)
      dawnduskrequest.setLocation(latitude, longitude)
      dawnduskrequest.calculateWithUTC(getutc)
      sunrise = dawnduskrequest.sunriseTime
      zenith = dawnduskrequest.meridianTime
      sunset = dawnduskrequest.sunsetTime
      dayduration =dawnduskrequest.durationTime
      if request[2] == "now" and dawnduskrequestelement == "all" :
          web.header('Content-Type', 'application/json')
          return json.dumps({"sunrise": sunrise, "zenith": zenith, "sunset": sunset, "dayduration": dayduration})
      if request[2] == "now" and dawnduskrequestelement == "sunrise" :
          if format == "json":
            web.header('Content-Type', 'application/json')
            return json.dumps({"sunrise": sunrise})
          else:
            return sunrise
      if request[2] == "now" and dawnduskrequestelement == "sunset" :
          if format == "json":
            web.header('Content-Type', 'application/json')
            return json.dumps({"sunset": sunset})
          else:
            return sunset
      if request[2] == "now" and dawnduskrequestelement == "zenith" :
          if format == "json":
            web.header('Content-Type', 'application/json')
            return json.dumps({"zenith": zenith})
          else:
            return zenith
      if request[2] == "now" and dawnduskrequestelement == "dayduration" :
          if format == "json":
            web.header('Content-Type', 'application/json')
            return json.dumps({"dayduration": dayduration})
          else:
            return dayduration
      if request[2] == "tomorrow" and dawnduskrequestelement == "all" :
          web.header('Content-Type', 'application/json')
          return json.dumps({"sunrise": sunrise, "zenith": zenith, "sunset": sunset, "dayduration": dayduration})
      if request[2] == "now" and dawnduskrequestelement == "sunrise" :
          if format == "json":
            web.header('Content-Type', 'application/json')
            return json.dumps({"sunrise": sunrise})
          else:
            return sunrise
      if request[2] == "tomorrow" and dawnduskrequestelement == "sunset" :
          if format == "json":
            web.header('Content-Type', 'application/json')
            return json.dumps({"sunset": sunset})
          else:
            return sunset
      if request[2] == "tomorrow" and dawnduskrequestelement == "zenith" :
          if format == "json":
            web.header('Content-Type', 'application/json')
            return json.dumps({"zenith": zenith})
          else:
            return zenith
      if request[2] == "tomorrow" and dawnduskrequestelement == "dayduration" :
          if format == "json":
            web.header('Content-Type', 'application/json')
            return json.dumps({"dayduration": dayduration})
          else:
            return dayduration

"""
@api {get} /weather/:city/:weatherrequest/:date/:responsetype Weather Status Request
@apiName GetWeather
@apiGroup Domogeek
@apiDescription Ask for weather (temperature, humidity, pressure, windspeed...) for :date in :city (France)
@apiParam {String} city City name (avoid accents, no space, France Metropolitan).
@apiParam {String} weatherrequest  Ask for {temperature|humidity[pressure|windspeed|weather|all}.
@apiParam {String} date  Date request {today | tomorrow}.
@apiParam {String} [responsetype]  Specify Response Type (raw by default or specify json, only for single element).
@apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {u'min': 15.039999999999999, u'max': 20.34, u'eve': 19.989999999999998, u'morn': 20.34, u'night': 15.039999999999999, u'day': 20.34}

     HTTP/1.1 200 OK
     {"pressure": 1031.0799999999999}

@apiErrorExample Error-Response:
     HTTP/1.1 400 Bad Request
     400 Bad Request

@apiExample Example usage:
     curl http://api.domogeek.fr/weather/brest/all/today
     curl http://api.domogeek.fr/weather/brest/pressure/today/json
     curl http://api.domogeek.fr/weather/brest/weather/tomorrow

"""

class weather:
    def GET(self,uri):
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /weather/city/{temperature|humidity|pressure|weather|windspeed|all}/{today|tomorrow}\n"
      try:
        city = request[0]
      except:
        return "Incorrect request : /weather/city/{temperature|humidity|pressure|weather|windspeed|all}/{today|tomorrow}\n"
      try:
        weatherrequestelement = request[1]
      except:
        return "Incorrect request : /weather/city/{temperature|humidity|pressure|weather|windspeed|all}/{today|tomorrow}\n"
      try:
        daterequest = request[2]
      except:
        return "Incorrect request : /weather/city/{temperature|humidity|pressure|weather|windspeed|all}/{today|tomorrow}\n"
      try:
        format = request[3]
      except:
        format = None
      if weatherrequestelement not in ["temperature", "humidity", "pressure", "weather", "windspeed", "all"]:
        return "Incorrect request : /weather/city/{temperature|humidity|pressure|weather|windspeed|all}/{today|tomorrow}\n"
      responsegeolocation = urllib2.urlopen(localapiurl+'/geolocation/'+city)
      resultgeolocation = json.load(responsegeolocation)
      try:
        latitude =  resultgeolocation["latitude"]
        longitude =  resultgeolocation["longitude"]
      except:
        return "NO GEOLOCATION DATA AVAILABLE\n"
      if request[2] == "today":
        todayweather = weatherrequest.todayopenweathermap(latitude, longitude, weatherrequestelement)
        if weatherrequestelement != "all" or weatherrequestelement != "temperature" or weatherrequestelement != "weather":
          if format == "json":
              web.header('Content-Type', 'application/json')
              if weatherrequestelement == "humidity":
                return json.dumps({"humidity": todayweather})
              if weatherrequestelement == "pressure":
                return json.dumps({"pressure": todayweather})
              if weatherrequestelement == "windspeed":
                return json.dumps({"windspeed": todayweather})
          else:
             return todayweather
        else:
            return todayweather
 
      if request[2] == "tomorrow":
        tomorrowweather = weatherrequest.tomorrowopenweathermap(latitude, longitude, weatherrequestelement)
        if weatherrequestelement != "all" or weatherrequestelement != "temperature" or weatherrequestelement != "weather":
          if format == "json":
              web.header('Content-Type', 'application/json')
              if weatherrequestelement == "humidity":
                return json.dumps({"humidity": tomorrowweather})
              if weatherrequestelement == "pressure":
                return json.dumps({"pressure": tomorrowweather})
              if weatherrequestelement == "windspeed":
                return json.dumps({"windspeed": tomorrowweather})
          else:
           return tomorrowweather
        else:
           return tomorrowweather

class MyDaemon(Daemon):
        def run(self):
          app.run()

if __name__ == "__main__":

        service = MyDaemon('/tmp/apidomogeek.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        sys.argv[1] =  listenip+':'+listenport
                        service.start()
                elif 'stop' == sys.argv[1]:
                        service.stop()
                elif 'restart' == sys.argv[1]:
                        service.restart()
                elif 'console' == sys.argv[1]:
                        sys.argv[1] =  listenip+':'+listenport
                        service.console()

                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart|console" % sys.argv[0]
                sys.exit(2)

