The makefile can generate two differnt executables `free_ener`, `free_ener_fixed`, and `MEMB_MC`, which respectively perform NC binding in the presence of undulating membranes, NC binding in the presence of fixed membranes, and equilibration of the membrane without the nanocarrier. Makefiles have been provided

```bash
make fe/fixed/memb
```

The executables are setup to run from inside the `RUNDIR`. The provided bash script can automatically do this for you. The runscript should be run as

```
bash runscript.sh free_ener 8 debug
```

Here `free_ener` is the executable to be run on `8` processors in the `debug` mode. In this mode, the code writes a certain number of statistical quantities to the screen which can be used to monitor the status the nanocarrier binding. This is not recommended for production runs which should be performed in the `silent` mode (If an option is not specified silent mode is enforced automatically).

# 24 Sep 15: Notes on the cutoff lengths used in the MC moves

The binding of the nanocarrier is very sensitive to the values of the various cutoff distances employed in the Monte Carlo simulations.

In our case, a number of parameters have been defined in the header of `movement.cpp`, which contains `void _movement :: bond_formation(int timestep)`. Given below are the parameters, their values and the rational for choosing them.

- Distance between the center of mass of the nanocarrier and any point on the membrane:

  `max_nc_memb_distance = pow(sqrt(2.0)*soft_radius,2);`

  This length is used to identify nanocarriers that have at least one vertex on the membrane within this cutoff

- The next distance is to identify all antigens on the membrane that can possibly form bonds with the antibodies on the nanocarrier:

  `max_nc_anttip_distance = pow(soft_radius+2.0*data.getmax_bond_stretch(),2);`

- The maximum distance between an antibody and the tip of an antigen is given by:

  `max_AB_ANT_distance = 2*pow(ant_size,2)*onemSqrt2;`

- The maximum stretch ($\Delta r$) of the Bell bond is set by the relation $lsnk_BT= \frac{1}{2}k_{\rm spring} \Delta r^2$ and this is defined in the code as:

  `Dreaction = pow(data.getmax_bond_stretch(),2);`

All the results I have were generated using these parameters. I have tested alternative values (smaller cutoffs) for these variables and found that the resulting PMF and energies from Thermodynamic integration were significantly different (and also unphysical) from those reported in our articles.
