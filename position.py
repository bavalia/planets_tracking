#!/usr/bin/python3

import math

#Descriptors
#http://stackoverflow.com/questions/3798835/understanding-get-and-set-and-python-descriptors

class PositionDescriptors(object):
  def __init__(self, notation='rec'):
    self.notation= notation

  def __get__(self, instance, owner):
    if self.notation=='rec':
      return (instance.x, instance.y, instance.z)
    elif self.notation=='spher':
      return owner.rec2spher(instance.x, instance.y, instance.z)

  def __set__(self, instance, value):
    setOn = 0
    if self.notation=='rec': setOn =1
    elif self.notation=='spher':
      value = instance.spher2rec(value[0],value[1],value[2])
      setOn =1

    if setOn :
      instance.x = float(value[0])
      instance.y = float(value[1])
      instance.z = float(value[2])


# help to build class
#http://www.rafekettler.com/magicmethods.html#descriptor
class Position(object):
  '''
  Positions are stored as Rectengular system in 
  Solar Ecliptic Coordinate System (SE)
  http://omniweb.gsfc.nasa.gov/coho/helios/plan_des.html 
  https://en.wikipedia.org/wiki/Ecliptic_coordinate_system
  '''
  #descriptors
  rec = PositionDescriptors('rec')
  spher = PositionDescriptors('spher')
  data = rec
  pol = spher

  def __init__(self, x=0, y=0, z=0):
    # All distances are in AU, astronomical unit
    self.x = float(x)
    self.y = float(y)
    self.z = float(z)

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
    distxy2 = px**2 + py**2
    dist = math.sqrt(distxy2 + pz**2)
    if distxy2!=0: lat = math.degrees(math.atan(pz/math.sqrt(distxy2)))
    elif pz==0: lat = 0.0
    elif pz>0: lat = 90.0
    elif pz<0: lat = -90.0

    if px!=0: lon = math.degrees(math.atan(py/px))
    elif py==0: lon = 0.0
    elif py>0: lon = 90.0
    elif py<0: lon =  270.0
    if px<0 : lon += 180.0
    lon = lon%360.0

    return (dist, lon, lat)

  # def rec(self):
  #   return (self.x, self.y, self.z)

  # def spher(self):
  #   return self.rec2spher(self.x, self.y, self.z)


#Inheritance of class
#def PositionFun(Position):
  # haven't implimented yet, #to-do



