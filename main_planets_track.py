#!/usr/bin/python3
'''
files: planets data, 

libraries: matplotlib, numpy

Online Planets data: create file for all planets on below NASA website
https://omniweb.gsfc.nasa.gov/coho/helios/planet.html

Mac OS X: ValueError: unknown locale: UTF-8 in Python, matplotlib 
add these lines to your ~/.bash_profile 
export LC_ALL=en_US.UTF-8 
export LANG=en_US.UTF-8
'''

import argparse
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

import vector # home made function for conversion between polar and rectangualar coordinates

def parseArgs():
  parser=argparse.ArgumentParser(description="Positions of planets on a given date in year 2016. \nDefault date is today. \n#to-do implement beyond 2016")
  parser.add_argument("date", type=str, nargs='?', help="date in format YYYY-MM-DD")
  return parser.parse_args()

def parseDate(date):
  return dt.datetime.strptime(date,'%Y-%m-%d')

def incrementDate(baseDate,deltaDays):
  return baseDate + dt.timedelta(deltaDays)

def ontype(event):
  '''response to key press'''
  print ("You pressed key:", event.key)
  global _date

  if (event.key == 'q'): quit()
  elif (event.key == 'enter'): _date= startDate
  elif (event.key == 'right'): _date= incrementDate(_date,1)
  elif (event.key == 'left'): _date= incrementDate(_date,-1)
  elif (event.key == 'up'): _date= incrementDate(_date,30)
  elif (event.key == 'down'): _date= incrementDate(_date,-30)
  elif (event.key == 'n'): # new date, #to-do key is captured before raw input
    tempDate = str(input("give a date in YYYY-MM-DD format: "))
    try : _date = parseDate(tempDate)
    except : print ('error in setting new date')

  position = getPosition(_yearlyData, _date)
  print ("new date: ",_date)
  #print (position)
  plotTheDay(position, _date)


def getPlanetsContant():
  data = {}
  data['name']= np.array(['Sun','mer','ven','ear','Mar','jup','sat','ura','nep'])
  data['color']= np.array(['yellow','gray','c','b','red','yellow','orange','c','c'])
  data['size']= np.array([80,20,35,50,20,50,40,20,20])
  data['dist']= np.array([0, 0.3871, 0.7233, 1.0, 1.5273, 5.2028, 9.5388, 19.1914, 30.0611])
  return data

def loadFile(planets,year):
  #np.array([np.array(data),'name',etc..],[],..])
  pData = []
  for i, planet in enumerate(planets):
    file= 'Planets data/'+str(year)+'/'+str(i+1)+'-'+planet+'.txt'
    lines = map(str.split, open(file).readlines()[1:])
    tempList = []
    for line in lines: tempList += [list(map(float, line[2:5]))]
    pData += [tempList]

  pData = np.array(pData, dtype='float64')
  sun = np.zeros(pData[0].shape, dtype='float64')

  return np.concatenate(([sun],pData),axis=0)

def fetchFile(planets,year):
  # fetches data from internet,
  # stores data in file
  # loadsFile
  print ("fetchFile function is not developed")

def getPosition(yearlyData, date):
  year = date.year
  planets = ['mer','ven','ear','mar','jup','sat','ura','nep']
  dayOfYear = date.timetuple().tm_yday

  try : 
    positionTable = yearlyData[year]
    #print ("found in cache")
  except :
    try : 
      print ("data is not availabe in cache for", year)
      # input:(dist, latDeg, lonDeg)
      temp = loadFile(planets,year)
      temp = temp[:,:,(0,2,1)]
      temp[:,:,(1,2)] = np.deg2rad(temp[:,:,(1,2)])
      positionTable = vector.pol2rec(temp)
      # output: (x,y,z)
    except : 
      print ("loading local file failed.") 
      try : 
        fetchFile(planets,year)
        temp = loadFile(planets,year)
        temp = temp[:,:,(0,2,1)]
        positionTable = vector.pol2rec(temp)
      except : 
        print ("LoadFile, fetchFile, getPosition funcitons failed. Quitting...")
        quit()
    yearlyData[year]=positionTable

  return positionTable[:,dayOfYear-1]

def setAxEcliptic(ax):
  ax.cla()
  #ax.axis('off')
  ax.set_xticks([0])
  ax.set_xticklabels(['20 June Solstice'])
  ax.set_yticks([-1,0,1])
  distMax = 5.5  # as distance will be used in squareroot.
  ax.axis([-distMax,distMax,-distMax,distMax])
  #ax.grid()


def setAxEarth(ax):
  ax.cla()
  ax.set_rmax(1.05)
  ax.autoscale(False)
  ax.set_rticks([])
  #xticks = np.linspace(0, np.pi*2, 12, endpoint=False)
  xticks = np.arange(0,np.pi*2,np.pi/6)
  label = ['W',20,22,0,2,4,'E',8,10,12,14,16]
  ax.set_xticks(xticks)
  ax.set_xticklabels(label)

def setAxConstellation(ax):
  ax.cla()
  ax.set_rmax(1.05)
  ax.autoscale(False)
  ax.set_rticks([])
  xticks = np.arange(0,np.pi*2,np.pi/6)
  label = ['       pisces','     aries','        taurus','gemini','cancer       ','leo   ','virgo     ','libra    ','scorpius         ','sagittarius','           capricorn','          aquarius']
  ax.set_xticks(xticks)
  ax.set_xticklabels(label)
  
def plotAxEcliptic(position, planetData, ax):
  # position in Rectangular form relative to The Sun
  temp = vector.rec2pol(position)
  temp[:,0] = np.sqrt(temp[:,0])
  pos = vector.pol2rec(temp)
  ax.scatter(pos[:,0],pos[:,1],planetData['size'],planetData['color'],clip_on=False)
  dist = np.sqrt(planetData['dist'])
  for i, r in enumerate(dist): 
    ax.add_patch(plt.Circle((0,0), radius=r, color=planetData['color'][i], fill=False))

def plotAxEarth(angleRad, planetData, ax):
  # position in Polar form relative to The Earth
  dist = np.full(len(angleRad), 1, dtype='int64')
  dist[3] = 0
  angle = (angleRad-angleRad[0]-np.pi/2)%(np.pi*2)
  ax.scatter(angle, dist, planetData['size'], planetData['color'], clip_on=False)
  dist = dist*.875
  ax.annotate('@12AM',(np.pi/2*3,.5),horizontalalignment='center')
  for i, name in enumerate(planetData['name']):
    ax.annotate(name[0],(angle[i],dist[i]),horizontalalignment='center',verticalalignment='center')

def plotAxConstellation(angleRad, planetData, ax):
  # position in Polar form relative to The Earth
  dist = np.full(len(angleRad), 1, dtype='int64')
  dist[3] = 0
  ax.scatter(angleRad, dist, planetData['size'], planetData['color'], clip_on=False)
  dist = dist*.875
  ax.annotate('Constellations',(np.pi/2*3,.5),horizontalalignment='center')
  for i, name in enumerate(planetData['name']):
    ax.annotate(name[0],(angleRad[i],dist[i]),horizontalalignment='center',verticalalignment='center')

def plotTheDay(position, date):
  #finding angle from earth for all planets and sun in Degree
  angleEarth = (vector.rec2pol(position-position[3]))[:,1]
  
  setAxEcliptic(_axEcliptic)
  _axEcliptic.set_title(date.strftime('%F'),horizontalalignment='center')
  plotAxEcliptic(position, _planetsConstant, _axEcliptic)

  setAxEarth(_axEarth)
  plotAxEarth(angleEarth, _planetsConstant, _axEarth)
  
  setAxConstellation(_axConstellation)
  plotAxConstellation(angleEarth, _planetsConstant, _axConstellation)

  plt.draw()
  #plt.pause(0.05)


if __name__=='__main__':
  ### get date
  args = parseArgs()

  try : startDate = parseDate(args.date)
  except : startDate = dt.datetime.now()
  _date = startDate
  print ('Date set to: '+startDate.strftime('%F %R'))

  ### get planets position data
  _planetsConstant = getPlanetsContant()
  _yearlyData = {}
  position = getPosition(_yearlyData, _date)
  print (position)

  ### Plot it, ax will be used as global data
  #http://matplotlib.org/users/gridspec.html
  _fig = plt.figure(figsize=(10,6))
  #fig.set_size_inches(10,6)
  _axEcliptic = plt.subplot2grid((2,3),(0,0), colspan=2, rowspan=2)
  _axEarth = plt.subplot2grid((2,3),(1,2), projection='polar')
  _axConstellation = plt.subplot2grid((2,3),(0,2), projection='polar')

  setAxConstellation(_axConstellation)
  setAxEarth(_axEarth)
  setAxEcliptic(_axEcliptic)

  plotTheDay(position, _date)
  _fig.canvas.mpl_connect('key_press_event',ontype)
  plt.show()
