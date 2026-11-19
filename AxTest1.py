# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 11:52:59 2026

@author: cwkan
"""
import numpy as np
import alpro
import matplotlib.pyplot as plt
alpro.util.set_default_plot_params()

test = alpro.test.RunTest()
test.test_analytic(subplot=111)



#### First Test with varying parameters, Mag field, length, etc.  
'''
import matplotlib.pyplot as plt
import numpy as np
import alpro
alpro.util.set_default_plot_params()
'''






s = alpro.Survival('uniform')
s.setup_regular_model(B= 1e-5, L=10, ne=0.0, N=1, phi=0.0)


    
s.set_params(g = 1e-12 * 1e-9, mass = 1e-11)  # set up ALP parameters in eV^-1 and eV
s.domain.B *=.01
energies = np.logspace(3,4,1000)               # energies in eV
s.propagate(energies=energies, pol="y")        # propagate the photon-ALP beam
fig = s.default_plot(theory = s.analytic_pga)  # this will compare to the analytic formula
plt.semilogy()


##### Before going onto more complicated magnetic fields and electron densities, try to start working on different propogations
'''
L = np.arange(1,100.1,10) # Array of lengths of propagation, 1-10 kpc through some mag field, analogous to start point of source in cloud

s = alpro.Survival('uniform')

for i in range(10):
    s.setup_regular_model(B= 1e-5, L=L[i], ne=0.0, N=1, phi=0.0)
    s.set_params(g = 1e-10 * 1e-9, mass = 1e-11)  # set up ALP parameters in eV^-1 and eV
    energies = np.logspace(3,4,1000)               # energies in eV
    s.propagate(energies=energies, pol="y")        # propagate the photon-ALP beam
    fig = s.default_plot(theory = s.analytic_pga, plot_kwargs={"label": "Legend"})  # this will compare to the analytic formula
    plt.semilogy()
    plt.legend()
'''
### New Goals: Plot at set energy over wide range of lengths, potentially 100 iterations, plot as survival rate of photon, not transformation probability, add all together and plot result, not each individual, potentially plot averaged/normalized version
'''
s = alpro.Survival('uniform')
s.setup_regular_model(B= 1e-5, L=3600, ne=0.0, N=1, phi=0.0)
s.set_params(g = 1e-12 * 1e-9, mass = 1e-11)  # set up ALP parameters in eV^-1 and eV
energies = np.logspace(3,4,1000)               # energies in eV
s.propagate(energies=energies, pol="y")        # propagate the photon-ALP beam
fig = s.default_plot( mode="survival")  # this will compare to the analytic formula
plt.semilogy()
plt.legend()
'''
#### Photon survivability for average sized galaxy cluster
'''
s = alpro.Survival('uniform')
energies = np.logspace(3,4,1000)               # energies in eV
Stot = np.zeros_like(energies)
Length = np.arange(1,3600.1,1)

for i in range(3600):
    s.setup_regular_model(B= 1e-5, L=Length[i], ne=.042, N=1, phi=0.0)
    s.set_params(g = 1e-12 * 1e-9, mass = 1e-11)
    s.propagate(energies=energies, pol="y")
    P = 1-s.P
    Stot += P

Stot = Stot/3600
plt.plot(energies, Stot)
plt.xscale('log')
plt.xlabel('E (eV)')
plt.ylabel(r"$P_{\gamma\gamma}$")
plt.title('Uniform model ne=.042')
'''

### Testing different electron densities, magnetic field models, and coherence lengths

### Going through electron densities with unifoirm mag field
'''
s = alpro.Survival('uniform')
s.setup_regular_model(B= 1e-5, L=10, ne=.1, N=1, phi=0.0)


    
s.set_params(g = 1e-12 * 1e-9, mass = 1e-12)  # set up ALP parameters in eV^-1 and eV
s.domain.B *=.01
energies = np.logspace(3,4,1000)               # energies in eV
s.propagate(energies=energies, pol="y")        # propagate the photon-ALP beam
fig = s.default_plot(theory = s.analytic_pga)  # this will compare to the analytic formula
plt.semilogy()
'''
### Trying out different magnetic field models, noteably the one used in prof reynolds' paper and libanov
'''
s = alpro.Survival("1275b")
s.init_model()
s.set_params(1e-12 * 1e-9, 1e-13)
Lmax = 2500.0
i = 0
s.domain.create_box_array(Lmax, i, s.coherence_func, r0=0)
plt.step(s.domain.rcen, s.domain.B * 1e6, where="mid")
plt.ylabel("$B_\perp (\mu G)$")
plt.xlabel("$z$ (kpc)")
energies = np.logspace(3,4,1000)
P, Pradial = s.propagate(s.domain, energies, pol="both")
fig = s.default_plot(plot_kwargs = {"lw": 3}, mode="survival")
'''