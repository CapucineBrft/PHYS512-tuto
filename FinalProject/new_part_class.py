#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 06:57:24 2020

@author: capucinebarfety
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class particle():
    """
    Class for the particle simulation. Contains methods to compute the density, Green function, potential and energy of the system.
    Also allows to evolve the system using the leapfrog method. Finally, it has a function to plot the 3D density grid and save it.
    Parameters:
        - pos: inital position of the particle(s). 
        - vel: inital velocity of the particle(s).
        - size: size of the density grid.
        - bound: type of boundary conditions. Choose 'periodic' or 'bounded'.
        - cosmology: whether to get the density from mass fluctuations prop to k^-3. Choose 'scale_inv' or None.
        - N: number of particles.
        - m: mass of the particles.
        - dt: time steps for the leapfrog integration.
        - soft: softenning parameter to ensure the potential does not blow up at r=0.
    
    """
    def __init__(self, pos, vel, size, bound, cosmology, N=1, m=1, dt=0.1, soft=4):
        
        self.size = size #size of the grid
        self.N = N #number of particles
        self.dt = dt #time step
        self.soft = soft #softening parameter
        self.bound = bound 
        self.cosmology = cosmology
    
            
        self.pos = np.transpose(pos) #position vector
        self.m = np.ones(self.pos.shape)*m #masses for each particules. Default is 1.
        
        
        
        #Creating the first density grid:
        #using an realization of k^-3:
        if self.cosmology == 'scale_inv':
            s1 = np.arange(self.size)
            box = np.meshgrid(s1, s1, s1)
            k = np.sqrt(box[0]**2 + box[1]**2 + box[2]**2)
            k[k == 0] = 1000000
            self.k = 1/(k**3)    
            self.grid = np.abs(np.fft.ifftn(self.k * np.fft.fftn(np.random.randn(self.size,self.size,self.size))))
        #Or using the "normal" method:
        else: 
            self.density()
            
        
        
            
        self.v = np.transpose(vel) #velocity vector
        self.green_f() #create Green's function
        self.coords = np.array([np.transpose(self.pos)[0], np.transpose(self.pos)[1], np.transpose(self.pos)[2]], dtype=int)
        
        
    def density(self):
        """
        Create the 3D density grid.
        """
        
        if self.N == 1:
            self.grid, self.edge = np.histogramdd(self.pos, 
                                    bins=(self.size, self.size, self.size), range=((0,self.size),(0,self.size),(0,self.size)))
        else:
            self.coords = np.array([np.transpose(self.pos)[0], np.transpose(self.pos)[1], np.transpose(self.pos)[2]], dtype=int)
            self.grid, self.edge = np.histogramdd((self.pos.T[0], self.pos.T[1], self.pos.T[2]), 
                                    bins=self.size, range=[[0,self.size],[0,self.size],[0,self.size]], weights= self.m[:,0])
    
        
        
    def green_f(self):
        """
        Compute Green's function for a single particle.
        """
        
        s1 = np.arange(self.size+1)
        s2 = s1[::-1][:-1]
        side = np.concatenate((s2,s1[:-1]))
        
        box = np.meshgrid(side, side, side)
       
        r = np.sqrt(box[0]**2 + box[1]**2 + box[2]**2)
        r[r < self.soft]  = self.soft
        self.green = -1/(4*np.pi*np.sqrt(r))
      
    
       
    def potential(self):
         """
         To get the potential, convolve the green's function with the density grid, i.e. multiply them in fourier space.
         """
         #Get FT:
         ft_green = np.fft.rfftn(self.green)
         
         grid = np.zeros((2*self.size, 2*self.size, 2*self.size)) #padding the density grid
         grid[0:self.size, 0:self.size, 0:self.size] = self.grid
         
         ft_grid = np.fft.rfftn(grid)
         
         #get the convolution:
         assert ft_green.shape == ft_grid.shape
         self.pot = np.fft.fftshift(np.fft.irfftn(ft_green * ft_grid))
         
         self.pot = self.pot[:self.size, :self.size, :self.size]
         
    
        
    
    def evolve(self):
        """
        Let the system evolve using a leapfrog scheme. 
        """
        
        self.potential()
        self.acc = -np.transpose(np.gradient(self.pot))
        
        self.density()
        self.pos = self.pos + self.v * self.dt
        
        
        #take into account boundary conditions. 
        #if periodic, bring back the ptcls on the other side of the grid
        if self.bound == 'periodic':
            self.pos = self.pos %(self.size-1)
        #if bounded, delete the particles that go outside the grid   
        if self.bound == 'bounded':
            ind_p = np.where(self.pos >= self.size)[0]
            ind_m = np.where(self.pos < 0)[0]
            ind = np.concatenate((ind_p, ind_m))
            #delete the particles that left the box from the positions
            self.pos = np.delete(self.pos, ind, axis=0)
            #delete them from the velocity:
            self.v = np.delete(self.v, ind, axis=0)
            #delete them from the masses:
            self.m = np.delete(self.m, ind, axis=0)
            
            
        self.coords = np.array([np.transpose(self.pos)[0], np.transpose(self.pos)[1], np.transpose(self.pos)[2]], dtype=int)
        self.v = self.v + self.acc[self.coords[2], self.coords[1], self.coords[0]] * self.dt/self.m

        self.density()
        self.potential()
        
     
        
     
    def total_E(self):
        """
        Keep track of the total energy of the system.
        """
        pot = -1/2 * np.sum(self.pot * self.grid)
        kinetic = 1/2 * np.sum(self.m * self.v**2)
        self.tot = pot + kinetic
        
        return self.tot
    
    

    def plot3d_rho(self, name):
        """
        3D plot of the density grid.
        """
        X, Y, Z = np.where(self.grid != 0)[0], np.where(self.grid != 0)[1], np.where(self.grid != 0)[2]
        fig = plt.figure()
        ax = Axes3D(fig)
        
        ax.set_ylim3d(0,self.size)
        ax.set_xlim3d(0,self.size)
        ax.set_zlim3d(0,self.size)
        ax.set_ylabel('y')
        ax.set_xlabel('x')
        ax.set_zlabel('z')
        
        ax.scatter(X, Y, Z, marker='.')
        #ax.view_init(90,90) #view from the top
        fig.savefig(f'{name}', dpi=100)   # save the figure to file
        plt.close(fig)
        

     
        
     
    
        

        
        
         
       
        
      
                
        

        
        
        
        
        