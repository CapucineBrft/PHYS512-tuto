#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 16:31:53 2020

@author: capucinebarfety
"""
from new_part_class import particle
import matplotlib.pyplot as plt
import numpy as np


if __name__=='__main__':
    # softening parameter
    soft = 2
    # size of the grid
    n = 20
    #number of iterations:
    it = 750
    #initial positions and velocities of the particles:
    pos = np.array([[10, 10],[7, 13], [10, 10]])
    #coord = np.array([pos[0], pos[1], pos[2]], dtype=int)
    v = np.array(([0.1,-0.1],[0,0],[0,0]))    
    
    
    # initialize the system
    p = particle(pos=pos,vel=v,size=n, N=2, soft=soft, dt=0.4, cosmology=None, bound='bounded', m = 1)
    
    p.potential()    
    p.acc = -np.transpose(np.gradient(p.pot))
    p.v += 0.5 * p.acc[p.coords[2], p.coords[1], p.coords[0]] * p.dt
    
    pp = []
    vv = []
    aa = []
    p.plot3d_rho('2ptcl_3dplots/0.png')
    
    Etot = []
    for i in range(1,it):
        
        p.evolve()
        p.plot3d_rho(f'2ptcl_3dplots/{i}.png')
        
        #record new x, y and z
        pp.append(p.pos)
        vv.append(p.v)
        aa.append(p.acc[p.coords[2], p.coords[1], p.coords[0]])
    
        
        
    #plt.plot(range(1,it), Etot)
    plt.figure(figsize=(8,8))
    plt.plot(np.transpose(pp)[0][0],np.transpose(pp)[1][0], 'r+', label='Ptcl 1')
    plt.plot(np.transpose(pp)[0][1],np.transpose(pp)[1][1], 'b.', label='Ptcl 2')
    plt.ylim(0, n)
    plt.xlim(0, n)
    plt.ylabel('y')
    plt.xlabel('x')
    plt.title('Particle positions at all times')
    plt.savefig('2ptcl_position.png')
    plt.legend()
