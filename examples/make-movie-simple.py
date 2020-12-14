from osiris_suite import OsirisDataContainer
from osiris_suite.plotting import *
from osiris_suite.computations import compute_fft_2d
import matplotlib.pyplot as plt 

import argparse 
import os 

# # uncomment this to enable command line options 
# parser = argparse.ArgumentParser() 
# parser.add_argument( '-d', dest = 'input_deck', default = './input.os', help = 'input deck path' )
# parser.add_argument( '-n', dest = 'nframes', default = 20, help = 'analysis script' )
# parser.add_argument( '-f', dest = 'frame', default = None, type = int, 
# 							help = 'specific frame to plot (default None)' )
# args = parser.parse_args() 

# data_path = os.path.dirname( os.path.abspath( args.input_deck ) )

# osdata = osiris_suite.OsirisDataContainer( data_path, args.input_deck )


data_path = './test-data/test-data-2d/'
input_deck_path = data_path + 'input.os'
osdata = OsirisDataContainer( data_path, input_deck_path )


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



plot_mgr_arr = [ [ e1_plot_mgr, e2_plot_mgr, e3_plot_mgr ] ]

# parameters to space the plots. fiddle with them until the plots 
# are spaced properly on your screen. 
subplots_adjust = (0.2, 0.5)

# could change timesteps here. a linear 
timesteps = osdata.data.ms.fld.e1.timesteps 

if len( timesteps ) <= 20 : 
	nframes = len( timesteps ) 
else : 
	nframes = 20 



suptitle = os.path.basename( os.getcwd() )

# when debugging, set the parameter show = 1 and keep killing the 
# program / modifying the inputs until you like it; then set show = 0
# to make all plots and generate the movie. 
osiris_suite.plotting.make_TS_movie( 	osdata, timesteps, 
									 	plot_mgr_arr, 
									 	suptitle = suptitle,
										global_modifier_function = None,
										subplots_adjust = subplots_adjust,
										savedir = './examples-output/make-movie-simple/',
										nframes = nframes,
										# show_index = args.frame,
										nproc = 12,
										duration = 5 )