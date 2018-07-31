#!/usr/bin/python3
'''
Description of function .
One file to rule them all.

usage: blah blah blah.
'''

#import argparse
#improt mechanize

import datetime
import math
#import copy
#import array

# help to build class
#http://www.rafekettler.com/magicmethods.html#descriptor
class Position(object):
  '''
  Positions are stored as Rectengular system in 
  Solar Ecliptic Coordinate System (SE)
  http://omniweb.gsfc.nasa.gov/coho/helios/plan_des.html 
  https://en.wikipedia.org/wiki/Ecliptic_coordinate_system
  '''
  def __init__(self, x=0, y=0, z=0):
    # All distances are in AU, astronomical unit
    self.x = x
    self.y = y
    self.z = z

  # Operator overloading
  #http://www.rafekettler.com/magicmethods.html
  def __sub__(self, other):
    return (self.x-other.x, self.y-other.y, self.z-other.z)

  def __neg__(self):
    return (-self.x, -self.y, -self.z)

  @staticmethod
  def spher2rec(dist, lon, lat):
    pz = dist * math.sin(math.radians(lat))
    distxy = dist * math.cos(math.radians(lat)) 
    py = distxy * math.sin(math.radians(lon))
    px = distxy * math.cos(math.radians(lon))
    return (px, py, pz)

  @staticmethod
  def rec2spher(px, py, pz):
    distxy = math.sqrt(px**2 + py**2)
    dist = math.sqrt(distxy**2 + pz**2)
    lat = math.degrees(math.atan(pz/distxy))

    lon = math.degrees(math.atan(py/px))
    if px<0.0 : lon += 180.0
    lon = lon%360.0

    return (dist, lon, lat)

  def rec(self):
    return (self.x, self.y, self.z)

  def spher(self):
    return self.rec2spher(self.x, self.y, self.z)


#Inheritance of class
#def PositionFun(Position):
  # haven't implimented yet, #to-do

def loadData(planets):
  '''
  loadData from local file downloaded from 
  http://omniweb.gsfc.nasa.gov/coho/helios/planet.html
  '''
  pData = {}
  i = 1
  for planet in planets:
    file= 'Planets data/2016/'+str(i)+'-'+planet+'.txt'
    lines = map(str.split, open(file).readlines()[1:])
    pData[planet] = []
    for line in lines: 
      pData[planet] += [list(map(float, line[2:5]))]
    i += 1

  return pData

def fromLocalData(planets,data, dayOfYear):
  pos = {}
  for planet in planets:
    fetch = data[planet][int(dayOfYear)-1]
    pos[planet] = Position(*(Position.spher2rec(fetch[0],fetch[2],fetch[1])))

  return pos


if __name__=='__main__':
  #temp variables, #to-do
  dayOfYear = datetime.date.today().strftime('%j')
  print (dayOfYear)
  earth = Position(*Position.spher2rec(1.017,288.16,0.0))
  mars = Position(*Position.spher2rec(1.459,268.45,-1.15))

  planets = ('mer','ven','ear','mar','jup','sat','ura','nep')
  localData = loadData(planets)

  planetsPos = fromLocalData(planets, localData, dayOfYear)

