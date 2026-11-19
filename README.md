# Perceus-Cluster-ALPPRO-Project
My files and calculations outlining my process of learning how to use ALRPO and applying it to the perceus cluster as a whole, integrating over entire lines of sight rather than independent cells to predict photon behavior

## AxTest1.py
This was simply a file using some of the premade ALPRO code to familiarize myself with the inputs, outputs, and now to work with the code. 

## simtest1.py
This was another introductory attempt at using the cell based modeling, just to familiarize myself with the code and what it would be most effective to use in the simulation

## Actual Sim.py
This is the code that I run and update most frequently, acting as the line of sight simulation through my simulated galaxy. I create an electron density profile for the galaxy, find the analogous magnetic field distribution, and run the simulation over an entire line of sight, from one side of the galaxy to the other where the observer is, integrating over 3600 one kiloparsec cells. I assume each of these cells is emitting light, hence why I integrate over each. The impact parameter of the line of sight can be adjusted by changing variable d, and results are weighted based on the square of the electron density, the mechanism behind the emission. 

## scaling test.py
This was my first baseline workthrough of what scaling this model would look like, working with random numbers to make a version of the simulation in which the resolution could be changed. Runthroughs typically take around 2.5 hours, so for quick checks something else was needed

## ScalingSim.py
This is the application of this scaling to the same simulation in the "Actual Sim" file. By changing scale factor SF, you can change how many cells the simulation is run through, with corresponding adjustments made to the electron density of each. 
