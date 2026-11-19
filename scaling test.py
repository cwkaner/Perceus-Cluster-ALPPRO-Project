# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 11:18:40 2026

@author: cwkan
"""
import numpy as np
#Scaling practice

A = np.arange(1,1000.1)
ne = np.random.random(np.size(A))

#If I want to scale it down from 1000 terms to an arbitrary number, make chunks and take average value within
#How would the coherence length apply here?
SF = 20 # Scale factor

choice = np.round(np.linspace(1,len(A)-1, num=SF+1)).astype(int)
NewL = A[choice]

# -----------------------Averaging over chunks--------------------------------
neresultsavg = np.zeros(len(NewL))


for i in range(len(NewL)):
    if i == 0:
        nenew = ne[0]
        neresultsavg[i] = nenew
    else:
        chunk = ne[int(NewL[i-1]):int(NewL[i])]
        nenew = np.mean(chunk)
        neresultsavg[i] = nenew


# -----------------------Maximum value for chunks--------------------------------

neresultsmax = np.zeros(len(NewL))


for i in range(len(NewL)):
    if i == 0:
        nenew = ne[0]
        neresultsmax[i] = nenew
    else:
        chunk = ne[int(NewL[i-1]):int(NewL[i])]
        nenew = np.max(chunk)
        neresultsmax[i] = nenew