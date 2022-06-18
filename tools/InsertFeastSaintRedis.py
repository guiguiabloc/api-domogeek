#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#
# Insert feasted saint day list in Redis
 
import csv
import sys
import hashlib
import redis

redis_host =  "127.0.0.1"
redis_port =  6379

rc= redis.Redis(host=redis_host, port=redis_port)
rc.set("test", "ok")
rc.expire("test" ,10)
value = rc.get("test")
if value is None:
  print ("Could not connect to  Redis  " + redis_host + " port " + redis_port)
  sys.exit(0) 

class TransformCSV(csv.Dialect):
    delimiter = ";"
    quotechar = None
    escapechar = None
    doublequote = None
    lineterminator = "\r\n"
    quoting = csv.QUOTE_NONE
    skipinitialspace = False

file = open("saintlist.csv", "rb")
print (file)
reader = csv.reader(file, TransformCSV())
print (reader)

def insertsaintdate():
  for row in reader:
      nameentry = row[0]
      dayentry = row [1]
      monthentry = row [2]
      group = dayentry+"-"+monthentry
      rediskeyfeastedsaint = hashlib.md5(group+"feastedsaint").hexdigest()
      value = rc.get(rediskeyfeastedsaint)
      if value is not None:
        newnameentry = ","+nameentry
        rc.append(rediskeyfeastedsaint, newnameentry)
      else:
        rc.set(rediskeyfeastedsaint, nameentry)

def insertsaintname():
  for element in reader:
      nameentry = element[0]
      nameentryok = str(nameentry.lower())
      dayentry = element[1]
      monthentry = element[2]
      group = dayentry+"-"+monthentry
      rediskeynamefeastedsaint = hashlib.md5(nameentryok+"feastedsaint").hexdigest()
      print ("NAME : "+nameentryok+ "HASH : "+rediskeynamefeastedsaint)
      rc.set(rediskeynamefeastedsaint, group)

###################
# Launch Function #
###################

insertsaintdate()
#insertsaintname()

