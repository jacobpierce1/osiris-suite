! scaled down pwfa simulation for local runs
simulation
{
  ! n0 = 1.74d21,
}

!----------the node configuration for this simulation---------
node_conf
{
  node_number(1:2) = 1,1,
  n_threads = 12,
  if_periodic(1:2) = .false., .false.,
}

!----------spatial grid----------
grid
{
  nx_p(1:2) = 256, 128,
  coordinates = "cartesian",
}

!----------time step and global data dump timestep number----------
time_step
{
  dt = 0.5,
  ! dt = 0.372,
  ndump = 10,
}

!----------restart information----------
restart
{
  ndump_fac = 0,
  if_restart = .false.,
}

!----------spatial limits of the simulations----------
!(note that this includes information about
! the motion of the simulation box)
space
{
  xmin(1:2) =  -256,    0.0,
  xmax(1:2) =    0,   256,
  if_move= .true., .false.,
}


!----------time limits ----------
time
{
  tmin = 0.0,
  tmax = 200.0,
}

!-----------electro-magnetic field------------------
! el_mag_fld
! {
! !  ifextfld = .true.,
! !  type_ext_e(2) = "math func",
! !  ext_e_mfunc(2) = 'if(x1>0, 5.747d-3/(x1/270.4+1)^2*x2, 0)',      ! start from x1=0
! }

!----------boundary conditions for em-fields ----------
emf_bound
{
  type(1:2,1) =  "vpml", "vpml",
  type(1:2,2) =  "vpml", "vpml",
}

!----------diagnostic for electromagnetic fields----------
diag_emf
{
  ndump_fac = 1,
  ndump_fac_ene_int = 1, 
  ndump_fac_ave = 0,
  ndump_fac_lineout = 0,
  reports = "e1", "e2", "e3"
}



!----------number of particle species----------
particles
{
  num_species = 1,
  interpolation = "linear",
}

species
{
  name = "electrons",
  push_type = "standard",
  rqm = -1,
  q_real = -1,
  num_par_x(1:2) = 2, 2, 
  num_par_max = 1e6,
}

udist
{
  uth(1:3) = 0.0, 0.0, 0.0,
  ufl(1:3) = 0.0, 0.0, 0.0,
}

profile
{
  density = 1,
  profile_type(1:2) = "piecewise-linear", "uniform",

  num_x = 4,
  x(1:4,1) = 0, 100, 150, 200,
  fx(1:4,1) = 0, 1, 1, 0,
}

spe_bound
{
  type(1:2,1) = "open", "open",
  type(1:2,2) = "open", "open",
}

diag_species
{
  ndump_fac = 1,
  ndump_fac_pha = 1,
  ndump_fac_ene = 1,
  reports = "charge", 
  phasespaces = "p2x1", "p1",
}

zpulse
{
  a0 = 1.0,
  if_launch = .true.,
  omega0 = 1.0,
  pol_type = 0,
  pol = 0.0,

  propagation = "forward",
  lon_type = "polynomial",
  lon_rise = 40,  ! FWHM_energy = 25 fs
  lon_fall = 40,
  lon_flat = 0,
  lon_start = 1.0,

  per_type = "gaussian",
  per_w0 = 40,  ! 10 um
  per_focus = 0.0,
}


current{}

diag_current
{
  ndump_fac = 1,
  ! reports = "j1", "j2", "j3" 
}

smooth
{
  type = "5pass",
}

! --------------------- end of osiris input file ---------------
