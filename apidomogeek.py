#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

import web, sys, time
import json
from datetime import datetime
import urllib, urllib2
from Daemon import Daemon
import Holiday

dayrequest = Holiday.jourferie()

urls = (
  '/holiday/(.*)', 'holiday',
  '/', 'index'
)

app = web.application(urls, globals())

class index:
    def GET(self):
        # redirect to the static file ...
        raise web.seeother('/static/index.html')


"""
@api {get} /holiday/:date Holiday Status Request
@apiName GetHoliday
@apiGroup Api.domogeek.fr
@apiDescription Ask to know if :date is a holiday
@apiParam {String} now  Ask for today.
@apiParam {String} all  Ask for all entry.
@apiParam {Datetime} D-M-YYYY  Ask for specific date.
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
     curl http://api.domogeek.fr/holiday/all
     curl http://api.domogeek.fr/holiday/25-12-2014

"""

class holiday:
    def GET(self,uri):
      request = uri.split('/')
      if request == ['']:
        web.badrequest()
        return "Incorrect request : /holiday/{now / date(D-M-YYYY)}\n"
      if request[0] == "now":
        datenow = datetime.now()
        year = datenow.year
        month = datenow.month
        day = datenow.day 
        result = dayrequest.estferie([day,month,year])
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
        return result


class MyDaemon(Daemon):
        def run(self):
          app.run()

if __name__ == "__main__":

        service = MyDaemon('/tmp/apidomogeek.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        sys.argv[1] =  '80'
                        service.start()
                elif 'stop' == sys.argv[1]:
                        service.stop()
                elif 'restart' == sys.argv[1]:
                        service.restart()
                elif 'console' == sys.argv[1]:
                        sys.argv[1] =  '80'
                        service.console()

                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart|console" % sys.argv[0]
                sys.exit(2)

