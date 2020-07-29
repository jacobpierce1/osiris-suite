
from osiris_suite import OsirisDataContainer
import osiris_suite.utils as utils 
import colorcet 
from pprint import pprint 
import numpy as np 
import os 
import sys 

import matplotlib
# matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import matplotlib.pyplot as plt 

from .plotter_utils import ffmpeg_combine, plot_2d_raw


def check_timesteps( leaves ) : 

	# verify timesteps 
	success = 1 

	# print( e_modes[0] )

	timesteps = leaves[0].timesteps
	indices = np.arange( len( timesteps ) )

	for leaf in leaves : 
		try : 
			success &= np.allclose( timesteps, leaf.timesteps ) 
		except : 
			success = 0 

	return success


def plot_q3d( data_path, index, savedir, title, nproc, 
				stride, duration   ) : 

	if savedir is None : 
		savedir = data_path + '/plots/q3d_summary/'

	frame_savedir = savedir + 'frames/'
	os.makedirs( frame_savedir, exist_ok = 1 )

	# load structure of the data tree (don't actually load data here)
	osdata = OsirisDataContainer( data_path, load_whole_file = True )

	print( osdata ) 

	# 	plot_q3d_globals( osdata ) 

	# if index is not None : 
	# 	plot_q3d_frame( osdata, index, savedir ) 

	leaves = []

	for m in range(3) : 
		key = 'mode_%d_re' % m 

		# check if this mode is present in data
		if not key in osdata.data.ms.fld : 
			break

		leaves.append( [] )

		leaves[m].append( osdata.data.ms.fld[key].e1_cyl_m )
		leaves[m].append( osdata.data.ms.fld[key].e2_cyl_m )
		leaves[m].append( osdata.data.ms.fld[key].e2_cyl_m )
		leaves[m].append( osdata.data.ms.density.electron[key].charge_cyl_m )



	leaves_flattened = [ leaves[i][j] for i in range( len(leaves))
						for j in range(len(leaves[i])) ]

	success = check_timesteps( leaves_flattened ) 

	if not success : 
		OSError( 'ERROR: timesteps for density and fields \
			are not aligned')

	print( 'info: entering plot q3D frame')

	indices = np.arange( len( leaves[0][0].timesteps ) )

	for index in indices[::stride] : 
		plot_q3d_frame( leaves, index, frame_savedir )

	movie_path = savedir + 'q3d_summary.mp4'
	ffmpeg_combine( savedir, movie_path )




def plot_q3d_globals( osdata ) : 

	osdata.load_hist() 


	... 



def plot_q3d_frame( leaves, index, frame_savedir ) : 

	timestep = leaves[0][0].timesteps[ index ] 

	nmodes = len( leaves )
	nleaves = len(leaves[0])
	axarr_shape  = (nmodes, nleaves )

	print( 'info: initializing ax')

	fig, axarr = plt.subplots( * axarr_shape, 
		figsize = (15, 3 * nmodes), squeeze = 0  )

	fig.subplots_adjust( hspace = 0.4, wspace = 0.4 )

	print( 'info: initialized ax')

	fig.suptitle( 't = %f' % timestep )

	titles = [ '$E_1$', '$E_2$', '$E_3$', '$n_e$' ]

	cmaps = [ colorcet.m_CET_D9, colorcet.m_CET_D9, colorcet.m_CET_D9,
				colorcet.m_rainbow  ]

	# loop thru modes and data
	for m in range( nmodes ) : 
		for i in range( nleaves ) : 

			title = titles[i] + ', m = %d' % m

			plot_2d_raw( fig, axarr[m,i], leaves[m][i], index, 
				cmaps[i], title )	

	path = frame_savedir + '/%03d' % index
	# plt.show()
	plt.savefig( path, dpi = 400 ) 
	plt.close() 



