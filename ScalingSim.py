# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 10:18:34 2026

@author: cwkan
"""

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




ne = nemod(r)
Esc = ne[1800,1775]
def bmod(ne):
    B = (7.5*10**(-6))*(ne/(Esc))**.5
    return B

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

#-----------------------------------------------------------------------------
#Setup Lengths and Electron Densities

d = 0 # slice of the cluster we are working with
nel = ne[(d+1800),:] ## Use first input to select 'y' value of line of sight through cluster, currently at center
Bd = B[(d+1800),:]
## 1800 is essentially (0,0) the reference for any inpact parameter


Length = np.arange(1,np.size(nel)+.1, 1)

nel2 = nel**2
weightnel = np.sum(nel2)

plt.plot(Length, nel)
plt.show()

#-----------------------------------------------------------------------------
#Scaling

SF = 200 # Scale factor, set to 3599 for full integration
block = Nx/SF #Length of new cells, for the delta L part of the integration
choice = np.round(np.linspace(1,len(Length)-1, num=SF+1)).astype(int)
LengthS = Length[choice]

# -----------------------Averaging over chunks--------------------------------
neavg = np.zeros(len(LengthS))


for j in range(len(LengthS)):
    if j == 0:
        nenew = nel[0]
        neavg[j] = nenew
    else:
        chunk = nel[int(LengthS[j-1]):int(LengthS[j])]
        nenew = np.mean(chunk)
        neavg[j] = nenew

Bavg = bmod(neavg)

neavg2 = neavg**2
weightnelavg = np.sum(neavg2)

#-----------------------------------------------------------------------------
#ALPRO SETUP


results = np.zeros((np.size(neavg), np.size(energies)))

for i in tqdm(range(np.size(neavg))):
    
    # Parameters
    Length1 = LengthS[0:len(LengthS)+1-i]
    s.initialise_domain()
    s.domain.ne = neavg[0:len(LengthS)+1-i]
    s.domain.B = Bd[0:Nx+1-i]
    s.domain.deltaL = block*np.ones(np.size(Length1))
    redge = np.cumsum(s.domain.deltaL)
    s.domain.phi = np.zeros(np.size(Length1))

    ### Use custome model option built in to create this profile
    s.set_params(g = 1e-12 * 1e-9, mass = 1e-13)
    s.propagate(energies=energies, pol="y")
    P = 1-s.P
    Stot += P*(neavg2[i]/weightnelavg)
    results[i] = P*(neavg2[i]/weightnelavg)
    
np.save("results_d={}_SF={}.npy".format(d,SF), results)
plt.plot(energies, Stot)
plt.xscale('log')
plt.xlabel('E (eV)')
plt.ylabel(r"$P_{\gamma\gamma}$")
plt.title('Custom model Beta model for ne, d={} SF={}'.format(np.abs(d), SF))
