from osiris_suite import OsirisDataContainer, OsirisSuiteError
import osiris_suite.utils
import colorcet 
import numpy as np 
import os 
import sys 
import glob 

import matplotlib
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits import axes_grid1


# matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import matplotlib.pyplot as plt 
import pathos.multiprocessing


# from .plotter_utils import ffmpeg_combine, plot_2d_raw




class PlotManager( object ) : 

	def __init__( self, data_getter, plotter, 
				modifier_function = None, ax = None ) : 

		self.data_getter = data_getter
		self.plotter = plotter 
		self.modifier_function = modifier_function
		# self.ax = ax 


	def plot( self, ax, timestep ) : 

		tmp = self.data_getter( timestep ) 
		
		if( tmp ) : 
			data, axes = tmp 

		else : 
			return 

		self.plotter.plot( ax, data, axes ) 

		if self.modifier_function is not None : 
			self.modifier_function( ax, data, axes ) 




class Plotter2D( object ) : 

	def __init__(	self, cmap = None, 
					logscale = 0, title = '', log_min = 1e-10 ) :
	
		if cmap is None : 
			self.cmap = colorcet.m_rainbow
		else : 
			self.cmap = cmap 

		self.logscale = logscale

		self.title = title

		self.log_min = log_min 


	def plot( self, ax, data, axes ) : 

		# if aspect is None : 
		# 	# aspect = data.shape[1] / data.shape[0]
		# 	aspect = ( axes[0][1] - axes[0][0] ) / ( axes[1][1] - axes[1][0] ) 
		# else : 
		# 	aspect = 'equal'

		aspect = ( axes[0][1] - axes[0][0] ) / ( axes[1][1] - axes[1][0] ) 

		extent = [axes[0][0], axes[0][1], axes[1][0], axes[1][1] ]

		norm = None
		
		if self.logscale : 

			data = np.abs( data )
			data = np.clip( data, self.log_min, None )
			norm = colors.LogNorm( vmin = data.min(), vmax = data.max() )

		im = ax.imshow( data.T, cmap = self.cmap, interpolation = 'bilinear', 
						origin = 'lower', aspect = aspect, extent = extent,
						norm = norm )



		# im = ax.pcolormesh( data, axes[0], axes[1], 
		# 						cmap = self.cmap, norm = norm )

		# divider = make_axes_locatable(ax)
		# cax = divider.append_axes( "right", size="5%", pad=0.05)
		# cax = fig.add_axes([ax.get_position().x1+0.005,ax.get_position().y0,0.02,ax.get_position().height])

		cb = plt.colorbar( im, ax = ax, fraction = 0.046, pad = 0.04 )

		# cb = plt.colorbar( im, ax = ax, fraction = 0.046, pad = 0.04, 
		# 					format =  '%.0e' )


		# cb = fig.colorbar( im, cax = cax ) # format = '%.1e' )
		# cb = add_colorbar( im ) 

		if not self.logscale :
			cb.formatter.set_powerlimits((0, 0))
		# cb.update_ticks()

		ax.set_title( self.title, pad = 20  )
		# ax.ticklabel_format( style = 'sci')


# currently does not work. probably could get this to work 
# if some time is put into it. 
class Plotter2DWithProjections( object ) : 

	def __init__(	self, cmap = None, 
					logscale = 0, title = '',
					avex = False, middlex = False,
					avey = False, middley = False ) :
	
		if cmap is None : 
			self.cmap = colorcet.m_rainbow
		else : 
			self.cmap = cmap 

		self.logscale = logscale
		self.title = title
		self.avex = avex 
		self.middlex = middlex
		self.avey = avey
		self.middley = middley 


	def plot( self, ax, data, axes ) : 

		aspect = ( axes[0][1] - axes[0][0] ) / ( axes[1][1] - axes[1][0] ) 

		extent = [axes[0][0], axes[0][1], axes[1][0], axes[1][1] ]

		norm = None
		
		if self.logscale : 

			data = np.abs( data )
			data = np.clip( data, 1e-10, None )
			norm = colors.LogNorm( vmin = data.min(), vmax = data.max() )

		im = ax.imshow( data.T, cmap = self.cmap, interpolation = 'bilinear', 
						origin = 'lower', aspect = aspect, extent = extent,
						norm = norm )
		
		# the padding works if the aspect is omitted as below, but then 
		# the padding is wrong. 
		# im = ax.imshow( data.T, cmap = self.cmap, interpolation = 'bilinear', 
		# 				origin = 'lower', extent = extent, # aspect = aspect, extent = extent,
		# 				norm = norm )


		cb = plt.colorbar( im, ax = ax, fraction = 0.046, pad = 0.04 )

		# # add lineouts 
		# # https://matplotlib.org/mpl_toolkits/axes_grid/users/overview.html
		# divider = make_axes_locatable( ax )

		# if self.avex or self.middlex : 
		# 	ax_xproj = divider.append_axes( "bottom", size="15%", pad=None, sharex=ax)
		# 	xaxis = np.linspace(  axes[0][1], axes[0][0], data.shape[0] )
		# 	if self.avex : 
		# 		ax_xproj.plot( xaxis, np.average( data, axis = 1 ), c='r' )
		# 	if self.middlex : 
		# 		ax_xproj.plot( xaxis, data[:,int(data.shape[1]/2)])

		# if self.avey or self.middley : 
		# 	ax_yproj = divider.append_axes( "left", size=1.2, pad=0.1, sharey=ax)


		if not self.logscale :
			cb.formatter.set_powerlimits((0, 0))

		ax.set_title( self.title )


class Plotter2DProj1D( object ) : 

	def __init__( self, logy = 0, title = '', ifvertical = False, axis = 0,
					ifplotave = False, ifplotmiddle = False, 
					ifplotidx = False, plotidx = 0, iflegend = False,
					xlabel = '', ylabel = '', aspect = None ) : 

		if axis not in [0, 1] : 
			raise OsirisSuiteError( 'ERROR: Plotter1DProjection currently only supports 2D input arrays') 

		self.logy = logy
		self.title = title 
		self.ifvertical = ifvertical
		self.axis = axis 
		self.ifplotave = ifplotave
		self.ifplotmiddle = ifplotmiddle
		self.ifplotidx = ifplotidx
		self.plotidx = plotidx 
		self.iflegend = iflegend 
		self.xlabel = xlabel 
		self.ylabel = ylabel 
		self.aspect = aspect 


	def plot( self, ax, data, axes ) : 

		if data.ndim != 2 : 
			raise OsirisSuiteError( 'ERROR: Plotter1DProjection currently only supports 2D input arrays') 
			
		xaxis = np.linspace(  axes[self.axis][0], 
					axes[self.axis][1], data.shape[self.axis] )

		ax.set_xlim( axes[self.axis][0], axes[self.axis][1] )

		if self.ifplotave : 
			aveaxis = 1 - self.axis
			ax.plot( xaxis, np.average( data, axis = aveaxis ), c='r',
						label = 'Average along %d' % aveaxis ) 
		
		if self.ifplotmiddle : 

			if self.axis == 0 : 
				data_slice = data[:, int(data.shape[1]/2)]
			else : 
				data_slice = data[int(data.shape[0]/2), :]

			ax.plot( xaxis, data_slice, label = 'Middle', c='b')
		
		if self.iflegend : 
			ax.legend( loc = 'best' )

		if self.xlabel : 
			ax.set_xlabel( self.xlabel ) 

		if self.ylabel : 
			ax.set_ylabel( self.ylabel ) 

		if self.aspect is not None : 
			xleft, xright = ax.get_xlim()
			ybottom, ytop = ax.get_ylim()
			ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*self.aspect)
			



class Plotter1D( object ) : 

	def __init__( 	self, multiple_data = False,
					colors = None, linestyles = None, labels = None,
					logy = 0, title = '' ) : 

		if not multiple_data : 
			colors = ( colors, )
			linestyles = ( linestyles, )
			labels = ( labels, )			

		self.multiple_data = multiple_data
		self.colors = colors 
		self.linestyles = linestyles 
		self.labels = labels 
		self.logy = logy
		self.title = title


	def plot( self, ax, data, axes ) : 

		# if multiple data are not supplied, package data into tuple
		# so we don't need to rewrite code below. 
		if not self.multiple_data : 
			data = (data,)
			axes = (axes,)

		for i in range( len( data ) ) : 

			c = None if self.colors is None else self.colors[i]
			linestyle = None if self.linestyles is None else self.linestyles[i]
			label = None if self.labels is None else self.labels[i]

			xaxis = np.linspace( axes[i][0][0], axes[i][0][1], len( data[i]) )

			ax.plot( xaxis, data[i], 
					 c = c, linestyle = linestyle, label = label )

		ax.set_title( self.title ) 

		if self.logy : 
			ax.set_yscale( 'log' )

		# else : 
		# 	ax.ticklabel_format( style = 'sci')
		if self.labels is not None : 
			ax.legend( loc = 'best' )



def raw_osdata_TS_data_getter( osdata_leaf, ndump_fac = 1 ) : 
	return lambda index :  osdata_leaf.file_managers[ index // ndump_fac ].unpack()



def raw_osdata_TS2D_plot_mgr( 	osdata_leaf, modifier_function = None, 
							cmap = None, logscale = 0, title = '',
							ndump_fac = 1 ) : 
		
	data_getter = raw_osdata_TS_data_getter( osdata_leaf, ndump_fac )
	plotter = Plotter2D( 	cmap = cmap, 	
							logscale = logscale, title = title )

	return PlotManager( data_getter, plotter, modifier_function )


def raw_osdata_TS1D_plot_mgr( 	osdata_leaf, modifier_function = None, 
								colors = None, linestyles = None, 
								labels = None,
								logy = 0, title = '',
								ndump_fac = 1 ) : 
		
	data_getter = raw_osdata_TS_data_getter( osdata_leaf, ndump_fac )
	
	plotter = Plotter1D( multiple_data = False,
						 colors = colors, 
						 linestyles = linestyles, 
						 labels = labels,
					     logy = logy, 
					     title = title )

	return PlotManager( data_getter, plotter, modifier_function )


# def TC1D_plot_mgr( data, axes, modifier_function = None, 
# 					cmap = None, logscale = 0, title = '' ) : 
		
# 	data_getter = lambda x : packaged_data

# 	plotter = Plotter1D( 	ax = None, cmap = cmap, 	
# 							logscale = logscale, title = title )

# 	return PlotManager( data_getter, plotter, modifier_function )





# def default_osiris_plotter( self, )



def ffmpeg_combine( plotdir, movie_name, duration ):
	pngfiles = glob.glob( plotdir + '/*.png' )
	nfiles = len( pngfiles ) 

	# frame_rate = min( 1, nfiles // duration )
	frame_rate = nfiles / duration
	command = 'ffmpeg -r %f -i %s%%*.png -vcodec libx264 -crf 25 -pix_fmt yuv420p -y %s' % ( 
    	frame_rate, plotdir, movie_name ) 
	print( command ) 
	os.system( command )



# def flatten_list( list_2d ) : 
#  	return [ list_2d[i][j] for i in range( len(list_2d))
# 						for j in range(len(list_2d[i])) ]




# def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
#     """Add a vertical color bar to an image plot."""
#     divider = axes_grid1.make_axes_locatable(im.axes)
#     width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
#     pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
#     current_ax = plt.gca()
#     cax = divider.append_axes("right", size=width, pad=pad)
#     plt.sca(current_ax)
#     return im.axes.figure.colorbar(im, cax=cax, **kwargs)



def make_frame( index, osdata, timesteps,
				shape, plot_mgr_arr, 
				suptitle = '', 
				figsize = None, subplots_adjust = None ) : 

	N, M = shape 

	if figsize is None : 
		figsize = ( 15, 9 )


	fig, axarr = plt.subplots( * shape, 
			figsize = figsize, squeeze = 0 )

	timestep_metadata = osdata.input_deck.get_metadata( 'time_step')
	dt = timestep_metadata[ 'dt' ]
	ndump = timestep_metadata[ 'ndump' ]

	abs_time = timesteps[ index ] * dt * ndump

	suptitle += '\n%.2f$\\omega_\\mathrm{pe}^{-1}$' % abs_time

	fig.suptitle( suptitle )

	# make all plots 
	for i in range( N ) : 
		for j in range( M ) :
			
			plot_mgr = plot_mgr_arr[i][j]
			
			if plot_mgr is not None : 
				plot_mgr.plot( axarr[i,j], timesteps[index])
			
			else : 
				fig.delaxes( axarr[i,j] ) 

	if subplots_adjust is not None : 
		hspace, wspace = subplots_adjust
		fig.subplots_adjust( hspace = hspace, wspace = wspace )

	# plt.tight_layout(h_pad=1)

	return fig, axarr 




def make_TS_movie(  osdata, timesteps,
					plot_mgr_arr, 
					suptitle = '', 
					figsize = None, subplots_adjust = None,
					savedir = None, 
					frame_startup_function = None,
					frame_cleanup_function = None,
					global_modifier_function = None,
					nproc = 1, nframes = 20, duration = 5,
					print_progress = True,
					show_index = None ) : 
	
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

	# success = check_leaf_timesteps( flatten_list( plot_mgr_arr ) ) 

	# if not success : 
	# 	raise OsirisSuiteError( 'ERROR: leaf timesteps are not aligned')

	show = show_index is not None

	shape = (len( plot_mgr_arr), len(plot_mgr_arr[0]))

	if show : 
		nproc = 1

	frame_savedir = savedir + '/frames/'
	os.makedirs( frame_savedir, exist_ok = 1 )

	files = glob.glob( frame_savedir + '*')

	for f in files:
		try:
			os.remove(f)
		except : 
			print("Error deleting file: %s " % (f ))


	timesteps = np.asarray( timesteps )

	spacing = int( len( timesteps ) / nframes ) # * ( timesteps[1] - timesteps[0])
	
	# indices = timesteps[ :: spacing ]
	indices = spacing * np.arange( nframes, dtype = int )

	print( 'INFO: plotting indices: ' + str( indices ) ) 
	print( 'INFO: corresponding abs times: ' + str( osdata.input_deck.get_abs_times( timesteps[ indices ] )) )

	if print_progress : 
		print( "Making movie..." )


	def handle_index( i ) : 

		index = indices[i]

		if print_progress : 
			print( "%d / %d" % ( i, len( indices ) ) )

		if frame_startup_function is not None : 
			frame_startup_function( index )

		fig, axarr = make_frame( index,
								 osdata, timesteps,
								 shape, plot_mgr_arr, 
								 suptitle, figsize, subplots_adjust )

		if global_modifier_function is not None : 
			global_modifier_function( fig, axarr ) 

		if frame_cleanup_function is not None : 
			frame_cleanup_function( index )

		path = frame_savedir + '/%03d' % i
		
		if show : 
			plt.show()

		else : 
			plt.savefig( path, dpi = 400 ) 
			plt.close() 


	if show : 
		handle_index( show_index )
		return 

	print( 'nproc: ', nproc ) 
	pool = pathos.multiprocessing.ProcessingPool( nproc ) 

	pool.map( handle_index, range( len( indices ) ) )	
	
	movie_path = ( savedir 
		+ os.path.basename( os.path.dirname( savedir ) ) 
		+ '.mp4' ) 

	print( 'Saving movie...' )

	ffmpeg_combine( frame_savedir, movie_path, duration )



