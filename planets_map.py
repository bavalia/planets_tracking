#!/usr/bin/python3
'''
files: getChar.py, position.py, planets data

usage: to map planets in 2016 year

Mac OS X: ValueError: unknown locale: UTF-8 in Python, matplotlib 
add these lines to your ~/.bash_profile 
export LC_ALL=en_US.UTF-8 
export LANG=en_US.UTF-8 
'''
#use numpy always; for faster development, runtime, support from matplotlib, easy to read and manipulate

#import argparse #to parse argument
#improt mechanize # to get data from net

import datetime
import math
#import time

#import copy
#import array
#import numpy as np
import matplotlib.pyplot as plt

import getChar
#personal file to get char/key press

from position import Position

def loadData(planets,year):
  '''
  loadData from local file downloaded from 
  http://omniweb.gsfc.nasa.gov/coho/helios/planet.html
  '''
  pData = {}
  i = 1
  for planet in planets:
    file= 'Planets data/'+str(year)+'/'+str(i)+'-'+planet+'.txt'
    lines = map(str.split, open(file).readlines()[1:])
    pData[planet] = []
    for line in lines: 
      pData[planet] += [list(map(float, line[2:5]))]
    i += 1

  return pData

def fromLocalData(planets,data, dayOfYear):
  pos = {'sun':Position(0,0,0)}
  for planet in planets:
    fetch = data[planet][dayOfYear-1]
    pos[planet] = Position(*(Position.spher2rec(fetch[0],fetch[2],fetch[1])))

  return pos

def plot2D(planetsPos, date):
  #http://matplotlib.org/api/pyplot_api.html
  # check 4dTo2d.py script for expample
  #http://matplotlib.org/examples/pylab_examples/subplots_demo.html

  plt.cla()
  global ax
  
  #ax = fig.gca()
  #ax.cla()
  #fig = plt.figure()
  #ax = fig.add_subplot(111)
  # ax = plt.gca() # get current axis
  

  #fig, ax = plt.subplots(1, subplot_kw=dict(projection='polar'))
  #plt.show(block=False)

  #ax.plot(theta, r, color='r', linewidth=3)
  
  axisLim = 10
  #ax.axis([-axisLim,axisLim,-axisLim,axisLim])
  ax.set_rmax(5.5)
  #ax.set_rscale('log')
  ax.autoscale(False)

  plt.title(str(date),horizontalalignment='right')
  #ax.set_title()
  #plt.draw()

  xs = []
  ys = []
  color = []
  size = []
  theta = []
  dist = []


  print ("\n### planet on: "+str(date)+" ###")
  for planet in planetsPos:
    loc = planetsPos[planet].rec
    xs += [loc[0]]
    ys += [loc[1]]

    loc = Position.rec2spher(*loc)
    print (planet,loc)
    theta += [math.radians(loc[1])%360.0]
    dist += [loc[0]**.5]
    color += ['c']
    size += [20]

    if planet == 'ear' : color[-1]='b';size[-1]=40
    elif planet == 'sun': color[-1]='y';size[-1]=50

  #ax.scatter(xs,ys,size,color)
  #ax.plot(theta, r, color='r', linewidth=3)
  ax.scatter(theta, dist, size, color,clip_on=False)
  plt.draw()
  plt.pause(0.05)
#  plt.draw()


def changePlot():
  key = getChar.getKey()
  global dayOfYear
  global planetsPos
  dayChange = 0

  if key=='left' or key=='down': 
    dayOfYear-=1
    dayChange = 1
  elif key=='right' or key=='up': 
    dayOfYear+=1
    dayChange = 1
  elif key=='enter': 
    dayOfYear = datetime.datetime.now().timetuple().tm_yday
    dayChange = 1
  elif key=='q': quit()

  if dayChange : 
    planetsPos = fromLocalData(planets, localData, dayOfYear)
    date = datetime.datetime(year, 1, 1) + datetime.timedelta(dayOfYear - 1)
    plot2D(planetsPos,date)




if __name__=='__main__':
  #temp variables, #to-do
  #dayOfYear = datetime.date.today().strftime('%j') #in string format
  dayOfYear =  datetime.datetime.now().timetuple().tm_yday #in int format
  print (dayOfYear)
  #earth = Position(*Position.spher2rec(1.017,288.16,0.0))
  #mars = Position(*Position.spher2rec(1.459,268.45,-1.15))

  planets = ('mer','ven','ear','mar','jup','sat','ura','nep')
  year = 2016
  localData = loadData(planets, year)

  planetsPos = fromLocalData(planets, localData, dayOfYear)
  #planetsPos['sun'] = Position(0,0,0)

  date = datetime.datetime(year, 1, 1) + datetime.timedelta(dayOfYear - 1)
  
  fig, ax = plt.subplots(1, subplot_kw=dict(projection='polar'))
  #plt.show(block=False)
  plt.ion()

  plot2D(planetsPos,date )


  for i in range(10) : changePlot()



