#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

import urllib,urllib2
from xml.dom.minidom import parseString
import json

class geolocation:

  def geogoogle(self, addr, api_key):
        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (urllib.quote(addr), urllib.quote(api_key))
        try:
          data = urllib.urlopen(url).read()
          datagoogle = json.loads(data)
        except urllib2.HTTPError, err:
          return False
        assert datagoogle['status'] == "OK"
        #print "CHECK GOOGLE"
        googleresult = json.dumps([s['geometry']['location'] for s in datagoogle['results']], indent=3)
        analyse = json.JSONDecoder()
        for part in analyse.decode(googleresult):
          latitude =  part['lat']
          longitude = part['lng']
          return latitude,longitude

  def geobing(self, addr, api_key):
       url = "http://dev.virtualearth.net/REST/v1/Locations?q=%s&key=%s" % (urllib.quote(addr), urllib.quote(api_key))
       try:
         data = urllib2.urlopen(url).read()
         databing = json.loads(data)
       except urllib2.HTTPError, err:
         return False
       assert databing['statusCode'] == 200
       #print "CHECK BING"
       bingresult = databing['resourceSets'][0]['resources']
       pointresult = [ city['point'] for city in bingresult ]
       coord = [ city['coordinates'] for city in pointresult ]
       latitude = coord[0][0]
       longitude = coord[0][1]
       return latitude,longitude
  
  def geonames(self, addr, api_key):
       url = "http://api.geonames.org/search?q=%s&maxRows=1&username=%s" % (urllib.quote(addr), urllib.quote(api_key))
       try:
         data = urllib2.urlopen(url).read()
       except urllib2.HTTPError, err:
         return "Error"
       dom = parseString(data)
       latTag = dom.getElementsByTagName('lat')[0].toxml()
       lngTag = dom.getElementsByTagName('lng')[0].toxml()
       latitude=latTag.replace('<lat>','').replace('</lat>','')
       longitude=lngTag.replace('<lng>','').replace('</lng>','')
       return latitude,longitude
        
