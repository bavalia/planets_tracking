#!/usr/bin/python3
'''
N dimention vector conversion using numpy library.
a numpy version of position.py
conversion between rectangular and polar coordinate system.
In polar coordinate, higher axis angles are -pi/2 to pi/2, like latitude.
# %timeit ans[ans==nan]=0  # to measure time of a funciton 
'''

import numpy as np

def rec2pol(vec):
  try: temp = vec.T
  except AttributeError: 
    ans = rec2pol(np.array(vec,dtype='float64'))
    if type(vec)==tuple: return tuple(ans)
    elif type(vec)==list: return list(ans)
    else : return ans
  
  ans = np.zeros(temp.shape)
  n = len(temp)
  if n<2 : ans = temp
  else :
    ans[0]= np.square(temp[0]) + np.square(temp[1])
    ans[1]= np.arctan(temp[1]/temp[0])
    if type(temp[0])==np.ndarray:
      ans[1,temp[0]<0]+=np.pi
    else : 
      if temp[0]<0 : ans[1]+=np.pi
    ans[1] = ans[1]%(np.pi*2)
    
    n -= 2
    for i in range(n):
      ans[-n+i] = np.arctan(temp[-n+i]/np.sqrt(ans[0]))
      ans[0] += np.square(temp[-n+i])

    ans[0] = np.sqrt(ans[0])
  
  #ans[ans==nan]=0
  isnan = np.isnan(ans)
  if np.any(isnan):
    #print ("nan encountered while converting rec2pol")
    ans[isnan]=0

  return ans.T


def pol2rec(vec):
  try: temp = vec.T
  except AttributeError: 
    ans = pol2rec(np.array(vec,dtype='float64'))
    if type(vec)==tuple: return tuple(ans)
    elif type(vec)==list: return list(ans)
    else : return ans

  ans = np.zeros(temp.shape)
  n = len(temp)
  temp[temp==np.nan]=0 #setting all nan to 0
  if n<2 : ans = temp
  else :
    ans[0] = temp[0]
    for i in range(n-1):
      ans[-i-1] = ans[0] * np.sin(temp[-i-1])
      ans[0] = ans[0] * np.cos(temp[-i-1])

  isnan = np.isnan(ans)
  if np.any(isnan):
    #print ("nan encountered while converting pol2rec")
    ans[isnan]=0

  return ans.T


if __name__=='__main__':
  pass
