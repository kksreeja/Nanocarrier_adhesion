#ifndef __FORTRAN_MODULES_H
#define __FORTRAN_MODULES_H
extern "C" void module_mcsmoves_mp_membrane_montecarlo();                         // declare the fortran subroutine performing the Monte Carlo moves for the membrane
extern "C" void module_mcsmoves_mp_membrane_montecarlo_biased();                  // declare the fortran subroutine performing the Monte Carlo moves for the membrane
extern "C" void module_mcsmoves_mp_link_flip();                                   // declare the fortran subroutine performing the Monte Carlo moves for the membrane
extern "C" void module_mcsmoves_mp_link_flip_biased();                            // declare the fortran subroutine performing the Monte Carlo moves for the membrane
extern "C" void module_mcsmoves_mp_vertex_move();                                 // declare the fortran subroutine performing the Monte Carlo moves for the membrane
extern "C" void module_mcsmoves_mp_vertex_move_biased();                          // declare the fortran subroutine performing the Monte Carlo moves for the membrane
extern "C" void module_mcsmoves_mp_antigen_diffusion_on_triangle();               // declare the fortran subroutine performing the Monte Carlo moves for the membrane
extern "C" void module_makesurface_mp_makesurface();
extern "C" void module_curvcalc_mp_compute_householdermatrix(int *, char *);      // Retrieve the HouseHolder Matrix for bond formation and breakage
extern "C" void module_curvcalc_mp_compute_antigen_orientation(int *);            // compute the polar and azimuthal angle for a chosen antigen
extern "C" void module_writedata_mp_write_membrane_xyz(int *,int *,int *);        // print membrane coordinates to a file
extern "C" void module_writedata_mp_write_membrane_area(int *, int *, int *);     // print membrane area to a file
extern "C" void module_writedata_mp_membrane_dump1(int *);                        // Dump the membrane files 
extern "C" void module_writedata_mp_membrane_dump2(int *, int *);                 // Dump the membrane files 
extern "C" void module_mcsmoves_mp_print_triangle_vert(int *);                  
extern "C" void module_mcsmoves_mp_print_image_vert(int *);                  
extern "C" int module_mcsmoves_mp_selfavoidance_allantigens();
extern "C" void module_datastruct_mp_interactive_shell();
extern "C" void module_mcsmoves_mp_antigen_hopping_on_vertex();
extern "C" void module_mcsmoves_mp_compute_flexed_base_tip_coord(int *);          // computes the base and tip coordinates of an antigen
extern "C" double module_datastruct_mp_compute_mean_membrane_z();                 // Compute mean height (z-value) of the membrane      
extern "C" void module_datastruct_mp_compute_mean_membrane_curvature(int *);      // Compute mean membrane curvature under the nanocarrier
extern "C" void module_datastruct_mp_store_restore_shadowvertices(int *,int *);   // Stores and Restores shadow vertices during NC move 
extern "C" void module_datastruct_mp_compute_nc_shadow_vertices(int *); 
extern "C" void module_datastruct_mp_ncshadow_r(int *);                           // compute mean r in the ncshadow.       
extern "C" double module_datastruct_mp_total_membrane_energy();
extern "C" double module_datastruct_mp_compute_closest_vertex(int*, double*, double*);
extern "C" double module_datastruct_mp_get_membrane_area();                       // function to get the membrane area
#endif
