# Final Project:

The class containing most of the work is inside the script named "new_part_class.py". This computes the potential of the particles by doing the convolution of Green's function with a density grid.

### Part 1:
The script to run the simulation for one particle at rest is "1particle.py". AS we can see in the gif "1ptcl" and the plot of x,y,z as function of time (1particle_position.png), a single particle at rest stays at rest.

### Part 2:
Thi script to run the simulation for 2 particles in orbit is "2particles.py". The gif "2ptcl" shows the  orbit viewed from the top in 3D. The plot "2ptcl_position.png" shows the evolution of their (x,y) positions. For them to be in a circular orbit, they need their initial velocity to be equal in strength but opposite in sign.

While they orbit each other, their motion is not perfectly circular.


### Part 3:
*Bounded*:
The script for boundary conditions where the particles can exit the box is underthe name "nbody_bounded.py". The 3D plot of the density grid evolving with time is shown in the gif "nbody_bounded". The total energy as a function of time is shown in "energy_bounded.py". As we can see, after the intial collision of all the particles, the energy is relatively stable, but slowly decreasing, probably due to the 'lost' particles that exited the box. The initial positions and velocities are random. 

*Periodic*:
The script for periodic boundary conditions is under the name "nbody_periodic.py". The difference is that when the position of the particles exceed the cell number, it is 'sent back' to other side of the grid.
The gif of the density evolution is shown in "nbody_periodic". The evolution of the total energy as function of time is shown in "energy_periodic.py". The graph is very similar to that of bounded BC, except without the small decay in energy at the end, because we are not losing any of the particles.

### Part 4:
The script for this part is "cosmology.py". The gif is "cosmo" and the plot of the energy is "energy_cosmo". I also included a plot of the intial density grid computed using the scale-invariant power spectrum, named "density_cosmo" (it is a collapsed 3D plot). 

The simulation does not behave the way I expected it to, as it doesn't form "filaments" in density. I couldn't find the reason why it behaves that way, but I suspect there is something wrong in my periodic boundary conditions, as I have the same sort of problem in Part 3.  
