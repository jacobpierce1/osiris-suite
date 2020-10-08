from osiris_suite import OsirisDataContainer, OsirisSuiteError
import osiris_suite.utils
import colorcet 
from pprint import pprint 
import numpy as np 
import os 
import sys 
import glob 

import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits import axes_grid1


# matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import matplotlib.pyplot as plt 
import pathos.multiprocessing


# from .plotter_utils import ffmpeg_combine, plot_2d_raw



def ffmpeg_combine( plotdir, movie_name, duration ):
	pngfiles = glob.glob( plotdir + '/*.png' )
	nfiles = len( pngfiles ) 

	# frame_rate = min( 1, nfiles // duration )
	frame_rate = nfiles / duration
	command = 'ffmpeg -r %f -i %s%%*.png -vcodec libx264 -crf 25 -pix_fmt yuv420p -y %s' % ( 
    	frame_rate, plotdir, movie_name ) 
	print( command ) 
	os.system( command )



def flatten_list( list_2d ) : 
 	return [ list_2d[i][j] for i in range( len(list_2d))
						for j in range(len(list_2d[i])) ]


def check_leaf_timesteps( leaves ) : 

	# verify timesteps 
	success = 1 

	timesteps = leaves[0].timesteps
	indices = np.arange( len( timesteps ) )

	for leaf in leaves : 
		
		if leaf is None : 
			continue 
		
		try : 
			success &= np.allclose( timesteps, leaf.timesteps ) 
		except : 
			success = 0 

	return success




def plot_image_raw( fig, ax, leaf, index, cmap, title ) : 

	if leaf is None : 
		return 

	data_mgr = leaf.file_managers[ index ]
	data_mgr.load() 
	data = data_mgr.data 
	axes = data_mgr.axes

	plot_image( fig, ax, data, cmap, title, axes )

	data_mgr.unload() 



def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)



def plot_image( fig, ax, data, cmap, title, axes, aspect = None ) : 

	if aspect is None : 
		# aspect = data.shape[1] / data.shape[0]
		aspect = ( axes[0][1] - axes[0][0] ) / ( axes[1][1] - axes[1][0] ) 
	else : 
		aspect = 'equal'

	extent = [axes[0][0], axes[0][1], axes[1][0], axes[1][1] ]

	im = ax.imshow( data, cmap = cmap, interpolation = 'bilinear', 
					origin = 'lower', aspect = aspect, extent = extent )

	# divider = make_axes_locatable(ax)
	# cax = divider.append_axes( "right", size="5%", pad=0.05)
	# cax = fig.add_axes([ax.get_position().x1+0.005,ax.get_position().y0,0.02,ax.get_position().height])

	cb = plt.colorbar( im, ax = ax, fraction = 0.046, pad = 0.04 )
	# cb = fig.colorbar( im, cax = cax ) # format = '%.1e' )
	# cb = add_colorbar( im ) 

	cb.formatter.set_powerlimits((0, 0))
	cb.update_ticks()

	ax.set_title( title )




def make_frame_raw( osdata, shape, leaves, 
					titles = None, cmaps = None, 
					suptitle = '', 
					figsize = None, subplots_adjust = None,
					index = -1 ) : 

	N, M = shape 

	if titles is None : 

		titles = np.empty( shape, dtype = str )

		for j in range(M): 
			for i in range(N) : 

				if leaves[i][j] is None : 
					continue

				titles[i,j] = leaves[i][j].file_managers[0].data_key 

	if cmaps is None : 
		cmaps = [[colorcet.m_rainbow 
					for j in range(M) ]
					for i in range(N) ]

	# print( cmaps ) 
	# print( titles ) 

	if figsize is None : 
		figsize = ( 15, 9 )


	fig, axarr = plt.subplots( * shape, 
			figsize = figsize, squeeze = 0  )

	timestep_metadata = osdata.input_deck.get_metadata( 'time_step')
	dt = timestep_metadata[ 'dt' ]
	ndump = timestep_metadata[ 'ndump' ]

	abs_time = leaves[0][0].timesteps[ index ] * dt * ndump

	if suptitle : 
		suptitle += ': '

	suptitle += '%.2f$\\omega_\\mathrm{pe}^{-1}$' % abs_time

	fig.suptitle( suptitle )

	for i in range( N ) : 
		for j in range( M ) :
			plot_image_raw( fig, axarr[i,j], leaves[i][j], index,
							cmaps[i][j], titles[i][j])

	if subplots_adjust is not None : 
		hspace, wspace = subplots_adjust
		fig.subplots_adjust( hspace = hspace, wspace = wspace )

	# plt.tight_layout(h_pad=1)

	return fig, axarr 




def make_movie( osdata, shape, leaves, 
				titles = None, cmaps = None, 
				suptitle = '', 
				figsize = None, subplots_adjust = None,
				savedir = None, modifier_function = None,
				nproc = 1, nframes = 20, duration = 5,
				print_progress = True,
				show = 0 ) : 
	
	'''
	generate plots and make a movie for a given set of OSIRIS data

	inputs: 
		osdata: already-loaded OsirisDataContainer
		...
		subplots_adjust: ( width, height ) to adjust plot spacing
		modifier_function: None or function with signature ( fig, axarr )
			which may modify fig and axarr at each timestep before plot is saved.
		nproc: number of processes to use. memory may be an issue. currently
			only multiprocessing within a single node is supported. 
		nframes: number of frames to use 
		duration: duration of output movie 
		print_progress: print messages about number of frames generated
		show: show the first plot and quit; don't generate other plots
			or save movie. 
	'''

	if not savedir : 
		raise OsirisSuiteError( 'ERROR: savedir must be specified' )

	success = check_leaf_timesteps( flatten_list( leaves ) ) 

	if not success : 
		raise OsirisSuiteError( 'ERROR: leaf timesteps are not aligned')

	if show : 
		nproc = 1

	frame_savedir = savedir + '/frames/'
	os.makedirs( frame_savedir, exist_ok = 1 )

	# this is a bug waiting to happen 
	# there may not be enough frames 
	
	indices = np.linspace( 0, len( leaves[0][0].timesteps ), nframes, 
							endpoint = False, dtype = int )

	print( indices ) 

	if print_progress : 
		print( "Making movie..." )


	def handle_index( i ) : 

		index = indices[i]

		if print_progress : 
			print( "%d / %d" % ( i, len( indices ) ) )

		fig, axarr = make_frame_raw( osdata, shape, leaves, titles, cmaps, 
								suptitle, figsize, subplots_adjust, 
								index )

		if modifier_function is not None : 
			modifier_function( fig, axarr ) 

		path = frame_savedir + '/%03d' % i
	
		if show : 
			plt.show()
		
		plt.savefig( path, dpi = 400 ) 
		plt.close() 

	if show : 
		handle_index( 0 )
		return 

	pool = pathos.multiprocessing.ProcessingPool( nproc ) 

	pool.map( handle_index, range( len( indices ) ) )	
	
	movie_path = ( savedir 
		+ os.path.basename( os.path.dirname( savedir ) ) 
		+ '.mp4' ) 

	print( 'Saving movie...' )

	ffmpeg_combine( frame_savedir, movie_path, duration )







