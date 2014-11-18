#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Gruik coded by GuiguiAbloc
# http://blog.guiguiabloc.fr
# http://api.domogeek.fr
#

from math import cos, acos, sin, asin, degrees, radians
import datetime

# Source:
# http://pagesperso-orange.fr/jean-paul.cornec/heures_lc.htm
# Special Thanks to arketip
class sunriseClass:
	def __init__(self):
		self.theDay=0
		self.theDate=[]
		self.solarDeclination=0
		self.equationOfTime=0
		self.latitude=0
		self.longitude=0
		self.sunrise=0
		self.sunset=0
		self.meridian=0
		self.duration=0
		self.sunriseTime=0
		self.sunsetTime=0
		self.meridianTime=0
		self.durationTime=0
	def getDay(self,d,m,y):
		d=float(d)
		m=float(m)
		y=float(y)
		n1 = int( (m* 275.0)/9.0 )
		n2 = int( (m+9.0)/12.0 )
		k = 1.0 + int( (y-4.0*int(y/4.0)+2.0)/3.0 )
		n=n1-n2*k+d-30.0
		return int(n)
	def getEoT(self,j):
		j=float(j)
		m = 357.0+(0.9856*j) 
		c = (1.914*sin(radians(m))) + (0.02*sin(radians(2.0*m)))
		l = 280.0 + c + (0.9856*j)
		r=(-2.465*sin(radians(2.0*l))) + (0.053*sin(radians(4.0*l)))
		Equ=(c+r)*4.0
		return Equ/60.0
	def getDec(self,j):
		j=float(j)
		m = 357.0+(0.9856*j) 
		c = (1.914*sin(radians(m))) + (0.02*sin(radians(2.0*m)))
		l = 280.0 + c + (0.9856*j)
		sinDec= 0.3978*sin(radians(l))
		return degrees(asin(sinDec))
	def getHo(self,Dec,Lat,Lon):
		cosHo=( -0.01454-sin(radians(self.solarDeclination))*sin(radians(self.latitude)) ) / ( cos(radians(self.solarDeclination))*cos(radians(self.latitude)) )
		return (degrees(acos(cosHo))/15.0)
	def setNumericalDate(self,d,m,y):
		self.theDate=[d,m,y]
		self.theDay=self.getDay(d,m,y)
		self.solarDeclination=self.getDec(self.theDay)
		self.equationOfTime=self.getEoT(self.theDay)
		return None
	def setLocation(self,Lat,Lon):
		self.latitude=Lat
		self.longitude=Lon
		return None
	def getHM(self,nH):
		h=int(nH)
		m=int(((nH*60.0)%60)+0.5)
                if m == 60 :
                   m = 00
                   h = h + 1
		return '%d:%02d' % (h,m)
	def calculateWithUTC(self,UTC):
		mLon=(self.longitude*4.0)/60.0
		Ho=self.getHo(self.solarDeclination,self.latitude,self.longitude)
		self.meridian=12.0+self.equationOfTime-mLon+UTC
		self.sunrise=self.meridian-Ho
		self.sunset=self.meridian+Ho
		self.duration=2.0*Ho
		self.meridianTime=self.getHM(self.meridian)
		self.sunriseTime=self.getHM(self.sunrise)
		self.sunsetTime=self.getHM(self.sunset)
		self.durationTime=self.getHM(self.duration)
		return None

