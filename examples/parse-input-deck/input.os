!--------the node configuration for this simulation--------
simulation
{
  !algorithm = "standard", 
  algorithm = "quasi-3D",
}

node_conf 
{
  node_number(1:2) =  1, 1,
  if_periodic(1:2) =  .true., .false.,
  n_threads = 12, 
}

!----------spatial grid----------
grid 
{
  nx_p(1:2) =  256, 256,
  coordinates = "cylindrical",
  n_cyl_modes = 2,
}

!----------time step and global data dump timestep number----------
time_step 
{
  dt     =   0.003125d0,
  ndump  =   10, 
}

!----------restart information----------
restart 
{
  ndump_fac = 0,
  if_restart = .false.,
}

!----------spatial limits of the simulations----------
space 
{
  xmin(1:2) =  0.000d0, 0.000d0,
  xmax(1:2) =  3.200d0, 3.200d0,
  if_move(1:2) = .false., .false.,
}

!----------time limits ----------
time 
{
  tmin = 0.0d0, tmax  = 7.0d0,
}

!----------field solver set up----------
el_mag_fld 
{
  solver = "fei",
}

!----------boundary conditions for em-fields ----------
emf_bound 
{
  type(1:2,1) =   "open", "open",
  type(1:2,2) =   "axial", "open",
}

emf_solver
{
  ! ---------------------------------------------------
  ! Example for a standard 4th order solver
  ! ---------------------------------------------------
  ! type = "standard",
  ! solver_ord = 4,

  ! ---------------------------------------------------
  ! Example for a 16th order bump solver with 16 solver
  ! coefficients. A perturbation of numerical dispersion
  ! relation is introduced between 0.1 kg1 to 0.3 kg1
  ! with relative strength 0.01, where kg1 = 2pi/dx1.
  ! ---------------------------------------------------
  type = "bump",
  solver_ord = 16,
  n_coef = 16,
  kl = 0.1,
  ku = 0.3,
  dk = 0.01,

  ! ---------------------------------------------------
  ! Example for a 2nd order Xu-type solver with 16 solver
  ! coefficients. For EM wave propagating in x1 in vacuum, 
  ! this solver is free of numerical dispersion relation.
  ! ---------------------------------------------------
  ! type = "xu",
  ! solver_ord = 2, ! lower order and high n_coef settings are recommended
  ! n_coef = 16,
  ! weight_n = 10, ! order of super-gaussian weight function.
  ! weight_w = 0.3, ! width of super-gaussian weight function. 0.3-0.4 is recommended

  ! ---------------------------------------------------
  ! Example for a 2nd order Dual type solver with 16 solver
  ! coefficients. This solver eliminate the numerical
  ! error caused by time stagger of E-field and B-field
  ! and simultaneously possesses the same numerical
  ! dispersion relation with Xu-type solver.
  ! ---------------------------------------------------
  ! type = "dual",
  ! solver_ord = 2, ! lower order and high n_coef settings are recommended
  ! n_coef = 16,
  ! weight_n = 10, ! order of super-gaussian weight function.
  ! weight_w = 0.3, ! width of super-gaussian weight function. 0.3-0.4 is recommended

  ! ---------------------------------------------------
  ! Example for a 4th order solver constructed by customizing
  ! the solver coefficients.
  ! ---------------------------------------------------
  ! solver = "customized-coef",
  ! n_coef = 2,
  ! coef_e(1:2) = 
  !  1.125000000000000,
  ! -0.041666666666667,
  ! coef_b(1:2) = 
  !  1.125000000000000,
  ! -0.041666666666667,

  ! ----------------------------------------------------
  ! low-pass spectral filter settings
  ! ----------------------------------------------------
  filter_limit = 0.6,
  filter_width = 0.1,
  n_damp_cell = 10,
  filter_current = .true.,
  
  ! ----------------------------------------------------
  ! current corrector, should be turned on for most cases
  ! ----------------------------------------------------
  correct_current = .true.,
}

diag_emf
{
  ndump_fac = 10,
  reports = "e1_cyl_m", "e2_cyl_m", "b1_cyl_m", "b2_cyl_m",
}


!----------number of particle species----------
particles
{
  interpolation = "quadratic",
  num_species = 1,
}

!----------information for species 1----------
species 
{
  name = "electron",
  num_par_max = 500000,
  rqm=-1.0,
  num_par_x(1:2) = 1, 1,
  num_par_theta = 8,
  push_type = "standard",
}

!----------inital proper velocities-----------------
udist
{
  uth(1:3) = 0.1d0, 0.1d0, 0.1d0,
  ufl(1:3) = 20.0d0, 0.0d0, 0.0d0,
}

!----------density profile for this species----------
profile 
{
  density = 1.0, 
}

!----------boundary conditions for this species----------
spe_bound 
{
  type(1:2,1) =   "open","open",
  type(1:2,2) =   "axial","open",
}

!----------diagnostic for this species----------
diag_species 
{
  ndump_fac = 1,
  reports = "charge_cyl_m",
}

current
{
}

! specify this section in conventional way when using digital filter
smooth
{
  type(1:2) = "none", "5pass",
}
