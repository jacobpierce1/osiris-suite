from osiris_suite import OsirisDataContainer
from osiris_suite.plotting import *
from osiris_suite.computations import compute_fft_2d

import colorcet 

data_path = './test-data/test-data-2d/'
input_deck_path = data_path + 'input.os'

osdata = OsirisDataContainer( data_path, input_deck_path = input_deck_path )
osdata.load_hist() 
osdata.load_timings()

shape = (2,4)

# example of using custom data for a plot, in this 
# case the spatial FFT of E2 
def e2_fft_computation( index ) : 

	e2 = osdata.data.ms.fld.e2
	data, axes = e2.file_managers[ index ].unpack()
	return osiris_suite.computations.compute_fft_2d( data )


# def make_energy_plot( ax, index ) : 

def energy_plot_data_getter( index ) : 

	data = []
	axes = []

	for key in [ 'E1', 'E2', 'E3' ] : 	
		fld_data = osdata.data.hist.fld_ene[ key ]
		fld_times = osdata.data.hist.fld_ene[ 'Time' ]
		data.append( fld_data )
		axes.append( [[ fld_times[0], fld_times[-1] ]] ) 

	electron_ke_data = osdata.data.hist.par01_ene[  'KinEnergy' ]
	electron_ke_times = osdata.data.hist.par01_ene[ 'Time' ]
	data.append( electron_ke_data )
	axes.append( [[electron_ke_times[0], electron_ke_times[-1] ]] )

	return data, axes  



dens_plot_mgr = raw_osdata_TS2D_plot_mgr( 
	osdata.data.ms.density.electrons.charge, 
	cmap = colorcet.m_rainbow, 
	logscale = 0, 
	title = 'Electron Density' )

e1_plot_mgr = raw_osdata_TS2D_plot_mgr( 
	osdata.data.ms.fld.e1, 
	cmap = colorcet.m_CET_D2, 
	logscale = 0, 
	title = 'E1' )

e2_plot_mgr = raw_osdata_TS2D_plot_mgr( 
	osdata.data.ms.fld.e2, 
	cmap = colorcet.m_CET_D2, 
	logscale = 0, 
	title = 'E2' )

e3_plot_mgr = raw_osdata_TS2D_plot_mgr( 
	osdata.data.ms.fld.e3, 
	cmap = colorcet.m_CET_D2, 
	logscale = 0, 
	title = 'E3' )

p2x1_plot_mgr = raw_osdata_TS2D_plot_mgr( 
	osdata.data.ms.pha.p2x1.electrons, 
	cmap = colorcet.m_CET_D2, 
	logscale = 0, 
	title = 'p2 vs. x1' )

p1_plot_mgr = raw_osdata_TS1D_plot_mgr( 
	osdata.data.ms.pha.p1.electrons, 
	colors = 'c',
	labels = 'p1',
	linestyles = '-.',
	logy = 0, 
	title = 'p1' )

e2_fft_plot_mgr = PlotManager( 
	data_getter = e2_fft_computation,
	plotter = Plotter2D( cmap = colorcet.m_fire, 
						 logscale = 0, 
						 title = 'FFT of E2') )

energy_plot_mgr = PlotManager( 
	data_getter = energy_plot_data_getter, 
	plotter = Plotter1D( multiple_data = True,
						 colors = 'rgbk', 
					 	 linestyles = '----',
						 labels = ['E1', 'E2', 'E3', 'Electron KE'],
						 title = 'Total energy vs. time',
						 logy = 1 ) )



plot_mgr_arr = \
[
	[ dens_plot_mgr, e1_plot_mgr, e2_plot_mgr, e3_plot_mgr ],
	[ p2x1_plot_mgr, p1_plot_mgr, e2_fft_plot_mgr, energy_plot_mgr ]
]


# example modifier function: optional function that can 
# be passed to dynamically modify the figure and array of plots
# after they've been created. this is a useful workaround to 
# avoid feature creep for the infinite number of simple custom
# options you might want for a plot. 

def global_modifier_function( fig, axarr ) : 

	axarr[0,0].set_ylabel( 'Spatial grid Data' )
	axarr[1,0].set_ylabel( 'Other data' ) 


# parameters to space the plots. fiddle with them until the plots 
# are spaced properly on your screen. 
subplots_adjust = (0.2, 0.5)

# could change timesteps here. a linear 
timesteps = osdata.data.ms.fld.e1.timesteps 

if len( timesteps ) <= 20 : 
	nframes = len( timesteps ) 
else : 
	nframes = 20 



# when debugging, set the parameter show = 1 and keep killing the 
# program / modifying the inputs until you like it; then set show = 0
# to make all plots and generate the movie. 
osiris_suite.plotting.make_TS_movie( 	osdata, timesteps, 
									 	plot_mgr_arr, 
										global_modifier_function = None,
										subplots_adjust = subplots_adjust,
										savedir = './examples-output/make-movie-advanced/',
										# show_index = 20,
										nproc = 12,
										duration = 5 )