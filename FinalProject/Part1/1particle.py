#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 19:15:21 2020

@author: capucinebarfety
"""
from new_part_class import particle
import matplotlib.pyplot as plt
import numpy as np



if __name__=='__main__':
    # softening parameter
    soft = 0.5
    # size of the grid
    n = 20
    #number of iterations:
    it = 10
    #number of particles:
    N = 1
    #initial positions and velocities of the particles:
    pos = np.transpose(np.random.rand(N,3) * n)
    #coord = np.array([pos[0], pos[1], pos[2]], dtype=int)
    v = np.random.rand(N,3) * 0
    # initialize the system
    p = particle(pos=pos,vel=v,size=n, N=N, soft=soft, dt=0.05, cosmology=None, bound='periodic')
    
    p.plot3d_rho('1ptcl_3dplots/0.png')
    
    x,y,z=[],[],[]
    x.append(p.coords[0])
    y.append(p.coords[1])
    z.append(p.coords[2])

    for i in range(1,10):
        #update the position and velocity
        p.evolve()
        p.plot3d_rho(f'1ptcl_3dplots/{i}.png')
        #record new x, y and z
        x.append(p.coords[0][0])
        y.append(p.coords[1][0])
        z.append(p.coords[2][0])
        

    #plot the time evolution of the coordinates
    fig = plt.figure()
    plt.plot(range(it), x, label='x')
    plt.plot(range(it), y, label='y')
    plt.plot(range(it), z, label = 'z')
    plt.title('Evoltuion of x,y,z coordinates with time')
    plt.xlabel('Iteration (time)')
    plt.ylabel('Coordinate')
    plt.legend()
    plt.savefig('1ptcl_position.png', dpi=150)
        