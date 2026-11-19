# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:30:58 2026

@author: cwkan
"""

#Plotting
import numpy as np
import matplotlib.pyplot as plt

Data = np.load('results_Bmod_d=0.npy')
weights = np.load('pointweights_Bmod_d=0.npy')
energies = np.logspace(3,4,1000)  

Fside = Data[0,:]
Nside = Data[3600,:]
Center = Data[1800,:]


plt.plot(energies, Fside)
plt.xlabel('Energies(eV)')
plt.ylabel('Photon Survival Probability')
plt.title('Survival Probability from emission furthest from observer')
plt.show()

plt.plot(energies, Nside)
plt.xlabel('Energies(eV)')
plt.ylabel('Photon Survival Probability')
plt.title('Survival Probability from emission closest to observer')
plt.xscale('log')
plt.yscale('log')
plt.show()

plt.plot(energies, Center)
plt.xlabel('Energies(eV)')
plt.ylabel('Photon Survival Probability')
plt.title('Survival Probability from center of cluster')
plt.show()
