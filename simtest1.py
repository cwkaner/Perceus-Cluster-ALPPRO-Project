import matplotlib.pyplot as plt
import numpy as np
import alpro
import time
alpro.util.set_default_plot_params()

def get_B(r):
    return (1e-5 * (r/25.0)**-0.5)

def get_ne(r):
    return (0.1 * (r/25.0)**-2)

# this controls the size of each random cell. Normally chosen using a power-law, but you can use
# any function or supply a float for a constant cell size
def coherence():
    return (np.random.random() * 10.0)

s = alpro.Survival("custom")      # initialise model

# set up get_B and density methods
s.cluster.get_B = get_B
s.cluster.density = get_ne


# initialise domain subclass using this profile
s.initialise_domain(s.cluster.profile)

# create a random cell model
s.domain.create_box_array(500.0, 1, coherence = coherence)

# plot the B model
_ = plt.step(s.domain.r, s.domain.Bx, where="pre")
_ = plt.step(s.domain.r, s.domain.By, where="pre")

energies = np.logspace(3,4,1000)
s.set_params(g = 1e-12 * 1e-9, mass = 1e-12)
s.propagate(energies=energies, pol="both")
fig = s.default_plot(mode="survival")