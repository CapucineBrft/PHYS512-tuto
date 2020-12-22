#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 14:53:38 2020

@author: capucinebarfety
"""
from new_part_class import particle
import matplotlib.pyplot as plt
import numpy as np


if __name__=='__main__':
    # softening parameter
    soft = 2
    # size of the grid
    n = 50
    #number of iterations:
    it = 300
    #number of particles:
    N = 10000
    #initial positions and velocities of the particles:
    pos = np.random.rand(3,N) * (n//2)
    v = np.random.randn(3,N)   
    
    
    # initialize the system
    p = particle(pos=pos,vel=v,size=n, N=N, soft=soft, dt=0.05, cosmology='scale_inv', bound='periodic')
    
    plt.figure()
    plt.imshow(p.grid.sum(axis=2), cmap='hot')
    plt.xlabel('y')
    plt.ylabel('x')
    plt.savefig('density_cosmo.png')
    
    
    p.potential()    
    p.acc = -np.transpose(np.gradient(p.pot))
    p.v += 0.5 * p.acc[p.coords[2], p.coords[1], p.coords[0]] * p.dt/p.m
    
    pp = []
    vv = []
    aa = []
        
    Etot = []
    for i in range(1,it):
        #evolve the system
        p.evolve()
        #compute the total energy of the system
        p.total_E()
    
        #get the #D plot of the density
        p.plot3d_rho(f'cosmo/{i}.png')
        
        #record new position, velocity, acceleration and energy
        pp.append(p.pos)
        vv.append(p.v)
        aa.append(p.acc[p.coords[2], p.coords[1], p.coords[0]])
        Etot.append(p.tot)
        
        
    plt.figure()
    plt.plot(range(1,it), Etot)
    plt.xlabel('Time')
    plt.ylabel('Total Energy')
    plt.title('Total Energy of the system as a function of time')
    plt.savefig('energy_cosmo.png')
