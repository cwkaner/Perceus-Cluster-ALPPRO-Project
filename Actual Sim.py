# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:54:20 2026

@author: cwkan
"""

import matplotlib.pyplot as plt
import numpy as np
import alpro
import time
from tqdm import tqdm

alpro.util.set_default_plot_params()

### Create grid and model of electron density to allow for adjusting of los
Nx = 3600
Ny = 3600
x = np.arange(-Nx/2,Nx/2 +.1,1)
y = np.arange(-Ny/2,Ny/2 +.1,1)

xx, yy = np.meshgrid(x,y)
r = np.sqrt(xx**2 +yy**2)



## Applying some more complicated electron densitiies

## Beta model
## Estimating central 'maximum' denisty based on persus cluster estimation in Prof Reynolds' paper

n0 = .042 # per cm^3, assuming this is what is used in simulations
Bet = 2/3 # Tentative set, actually based on other thijngs in this model
rc = 340 # core radius, rough estimate, dont need anything perfect yet

def nemod(r):
    ne = n0*(1+(r/rc)**2)**(-3*(Bet)/2)
    return ne

def bmod(ne):
    B = (7.5*10**(-6))*(ne/(ne[1800,1775]))**.5
    return B


ne = nemod(r)
B = bmod(ne)




h = plt.contourf(x,y,ne, 30)
plt.axis('scaled')
plt.title('Beta-model electron density dist')
plt.colorbar()
plt.show()

h = plt.contourf(x,y,ne)
plt.axis('scaled')
plt.title('Beta-model electron density dist')
plt.colorbar()
plt.show()

# ----------------------------------------------------------------------------
# Begin ALPRO Section

s = alpro.Survival('custom')
energies = np.logspace(3,4,1000)               # energies in eV
Stot = np.zeros_like(energies)

d = 600 # slice of the cluster we are working with
nel = ne[(d+1800),:] ## Use first input to select 'y' value of line of sight through cluster, currently at center
Bd = B[(d+1800),:]
## 1800 is essentially (0,0) the reference for any inpact parameter


Length = np.arange(1,np.size(nel)+.1, 1)

nel2 = nel**2
weightnel = np.sum(nel2)

plt.plot(Length, nel)
plt.show()

results = np.zeros((np.size(nel), np.size(energies)))
ptwghts = np.zeros((np.size(nel), np.size(energies)))

for i in tqdm(range(np.size(nel))):
    
    # Parameters
    Length1 = Length[0:Nx+1-i]
    s.initialise_domain()
    s.domain.ne = nel[0:Nx+1-i]
    s.domain.B = Bd[0:Nx+1-i]
    s.domain.deltaL = np.ones(np.size(Length1))
    redge = np.cumsum(s.domain.deltaL)
    s.domain.phi = np.zeros(np.size(Length1))

    ### Use custome model option built in to create this profile
    s.set_params(g = 1e-12 * 1e-9, mass = 1e-13)
    s.propagate(energies=energies, pol="y")
    P = 1-s.P
    ptwghts[i] = nel2[i]
    Stot += P*(nel2[i]/weightnel)
    results[i] = P*(nel2[i]/weightnel)
    
np.save("results_Bmod_d={}.npy".format(d), results)
np.save("pointweights_Bmod_d={}.npy".format(d), ptwghts)
plt.plot(energies, Stot)
plt.xscale('log')
plt.xlabel('E (eV)')
plt.ylabel(r"$P_{\gamma\gamma}$")
plt.title('Custom model Beta model for ne, d={}'.format(np.abs(d)))