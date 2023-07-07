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


class PlotManager( object ) : 

	def __init__( self, data_getter, plotter, 
				modifier_function = None, ax = None ) : 

		self.data_getter = data_getter
		self.plotter = plotter 
		self.modifier_function = modifier_function


	def plot( self, ax, timestep ) : 

		tmp = self.data_getter( timestep ) 
		
		if( tmp ) : 
			data, axes = tmp 

		else : 
			return 

		self.plotter.plot( ax, data, axes ) 

		if self.modifier_function is not None : 
			self.modifier_function( ax, data, axes, timestep ) 




class Plotter2D( object ) : 

	def __init__(	self, **kwargs ) :

		try :
			self.bounds = kwargs[ 'bounds' ]
		except :
			self.bounds = None

		try :
			self.vmin = kwargs['vmin']
		except :
			self.vmin = None

		try :
	       		self.vmax = kwargs['vmax']
		except :
			self.vmax = None

		try :
	       		self.if_abs = kwargs['if_abs']
		except :
			self.if_abs = False

		try :
	       		self.sym_logscale = kwargs['sym_logscale']
		except :
			self.sym_logscale = False

		try :
	       		self.use_divnorm = kwargs['use_divnorm']
		except :
			self.use_divnorm = False

		try :
	       		self.logscale = kwargs['logscale']
		except :
			self.logscale = False

		try :
	       		self.log_min = kwargs['log_min']
		except :
			self.log_min = None
			
		try :
	       		self.title = kwargs['title']
		except :
			self.title = ''

		try :
	       		self.xlabel = kwargs['xlabel']
		except :
			self.xlabel = ''

		try :
	       		self.ylabel = kwargs['ylabel']
		except :
			self.ylabel = ''

		try :
	       		self.add_cbar = kwargs['add_cbar']
		except :
			self.add_cbar = True

		try :
	       		self.cbar_label = kwargs['cbar_label']
		except :
			self.cbar_label = ''
			
		try :
	       		self.cmap = kwargs['cmap']
		except :
			self.cmap = colorcet.m_rainbow

		try :
	       		self.interpolation = kwargs['interpolation']
		except :
			self.interpolation = None
			
		try :
			self.transpose = kwargs[ 'transpose' ]
		except :
			self.transpose = False

		try :
			self.flipaxis = kwargs[ 'flipaxis' ]
		except :
			self.flipaxis = None

		
		
		
	def plot( self, ax, data, axes ) : 

		# if aspect is None : 
		# 	# aspect = data.shape[1] / data.shape[0]
		# 	aspect = ( axes[0][1] - axes[0][0] ) / ( axes[1][1] - axes[1][0] ) 
		# else : 
		# 	aspect = 'equal'
		axes = np.asarray( axes ) 
		new_axes = np.copy( axes ) 

		ops = [ max, min ]

		if self.bounds is not None : 
			for i in range(2) : 
				for j in range(2) : 
					if self.bounds[i][j] is not None : 
						new_axes[i,j] = ops[j]( new_axes[i,j], self.kwargs['bounds'][i][j] )

			dx = ( axes[:,1] - axes[:,0] ) / data.shape
			imin = np.floor( (new_axes[:,0] - axes[:,0]) / dx ).astype( int ) 
			imax = np.floor( (new_axes[:,1] - axes[:,0]) / dx ).astype( int ) 

			data = data[ imin[0] : imax[0], imin[1] : imax[1] ]

		else : 
			new_axes = axes 

		if self.transpose : 
			data = data.T 

		if self.flipaxis is not None  :
			data = np.flip( data, axis = self.flipaxis ) 
			
		aspect = ( new_axes[0][1] - new_axes[0][0] ) / ( new_axes[1][1] - new_axes[1][0] ) 

		extent = [new_axes[0][0], new_axes[0][1], new_axes[1][0], new_axes[1][1] ]

		norm = None

		if( self.if_abs ) : 
			data = np.abs( data )
		
		if self.vmin is None : 
			vmin = np.nanmin( data )
		else : 
			vmin = self.vmin 

		if self.vmax is None : 
			vmax = np.nanmax( data )
		else : 
			vmax = self.vmax 

		if self.sym_logscale : 
			
			if self.use_divnorm : 
				# norm = TwoSlopeSymLogNorm( self.log_min, vmin = data.min(), vmax = data.max() )
					
				vmax = max( vmax, abs(vmin) )

				norm = colors.SymLogNorm( self.log_min, vmin = -vmax, vmax = vmax, base = 10 )
				# todo: use TwoSlopeSymLogNorm

			else : 
				norm = colors.SymLogNorm( self.log_min, vmin = vmin, vmax = vmax, base = 10 )

		elif self.logscale : 

			data = np.abs( data )
			data = np.clip( data, self.log_min, None )

			if self.vmax is None : 
				vmax = data.max() 

			# norm = colors.LogNorm( vmin = vmin, vmax = vmax )
			norm = colors.LogNorm( vmin = self.log_min, vmax = vmax )

		# lin scale 
		else : 

			if self.use_divnorm and vmax != 0 and vmin != 0 : 

				# for matplotlib 3.2+ 
				try : 
					norm_class = colors.TwoSlopeNorm 
				
				# for earlier versions 
				except : 
					norm_class = colors.DivergingNorm

				# only one of these can be true 
				if vmax < 0 : 
					vmax = abs(vmin) 

				if vmin > 0 : 
					vmin = -abs(vmax) 

				# if vmax == 0 : 
				# 	vmax = 1 

				# if vmin == 0 : 
				# 	vmin = -1 

				norm = norm_class( vmin = vmin, vcenter = 0.0, vmax = vmax )
				
			else : 

				norm = colors.Normalize( vmin = vmin, vmax = vmax )

		im = ax.imshow( data.T, cmap = self.cmap, interpolation = self.interpolation, 
						origin = 'lower', aspect = aspect, extent = extent,
						norm = norm )

		if self.add_cbar : 
			cb = plt.colorbar( im, ax = ax, fraction = 0.046, pad = 0.04 )

			if not ( self.logscale or self.sym_logscale )  :
		
				cb.formatter.set_powerlimits((0, 0))

		# ax.set_title( self.title, pad = 20  )

		labelsize = 18

		if self.title : 
			ax.set_title( self.title)

		if self.xlabel : 
			ax.set_xlabel( self.xlabel, fontsize = labelsize ) 

		if self.ylabel : 
			ax.set_ylabel( self.ylabel, fontsize = labelsize ) 

		if self.add_cbar : 
			if self.cbar_label : 
				cb.set_label( self.cbar_label, fontsize = labelsize )


		# ax.ticklabel_format( style = 'sci')


# # currently does not work. probably could get this to work 
# # if some time is put into it. 
# class Plotter2DWithProjections( object ) : 

# 	def __init__(	self, cmap = None, 
# 					logscale = 0, title = '',
# 					avex = False, middlex = False,
# 					avey = False, middley = False ) :
	
# 		if cmap is None : 
# 			self.cmap = colorcet.m_rainbow
# 		else : 
# 			self.cmap = cmap 

# 		self.logscale = logscale
# 		self.title = title
# 		self.avex = avex 
# 		self.middlex = middlex
# 		self.avey = avey
# 		self.middley = middley 


# 	def plot( self, ax, data, axes ) : 

# 		aspect = ( axes[0][1] - axes[0][0] ) / ( axes[1][1] - axes[1][0] ) 

# 		extent = [axes[0][0], axes[0][1], axes[1][0], axes[1][1] ]

# 		norm = None
		
# 		if self.logscale : 

# 			data = np.abs( data )
# 			data = np.clip( data, 1e-10, None )
# 			norm = colors.LogNorm( vmin = data.min(), vmax = data.max() )

# 		im = ax.imshow( data.T, cmap = self.cmap, interpolation = 'bilinear', 
# 						origin = 'lower', aspect = aspect, extent = extent,
# 						norm = norm )
		
# 		# the padding works if the aspect is omitted as below, but then 
# 		# the padding is wrong. 
# 		# im = ax.imshow( data.T, cmap = self.cmap, interpolation = 'bilinear', 
# 		# 				origin = 'lower', extent = extent, # aspect = aspect, extent = extent,
# 		# 				norm = norm )


# 		cb = plt.colorbar( im, ax = ax, fraction = 0.046, pad = 0.04 )

# 		# # add lineouts 
# 		# # https://matplotlib.org/mpl_toolkits/axes_grid/users/overview.html
# 		# divider = make_axes_locatable( ax )

# 		# if self.avex or self.middlex : 
# 		# 	ax_xproj = divider.append_axes( "bottom", size="15%", pad=None, sharex=ax)
# 		# 	xaxis = np.linspace(  axes[0][1], axes[0][0], data.shape[0] )
# 		# 	if self.avex : 
# 		# 		ax_xproj.plot( xaxis, np.average( data, axis = 1 ), c='r' )
# 		# 	if self.middlex : 
# 		# 		ax_xproj.plot( xaxis, data[:,int(data.shape[1]/2)])

# 		# if self.avey or self.middley : 
# 		# 	ax_yproj = divider.append_axes( "left", size=1.2, pad=0.1, sharey=ax)


# 		if not self.logscale :
# 			cb.formatter.set_powerlimits((0, 0))

# 		ax.set_title( self.title )

class PlotManagerStack( object ) : 

	def __init__( self, plot_mgr_list ) : 

		self.plot_mgr_list = plot_mgr_list

	def plot( self, ax, timestep ) : 

		for plot_mgr in self.plot_mgr_list : 

			plot_mgr.plot( ax, timestep )

		# tmp = self.data_getter( timestep ) 
		
		# if( tmp ) : 
		# 	data, axes = tmp 

		# else : 
		# 	return 

		# self.plotter.plot( ax, data, axes ) 

		# if self.modifier_function is not None : 
		# 	self.modifier_function( ax, data, axes ) 

class Plotter2DProj1D( object ) : 

	def __init__( self, **kwargs ) :

		try :
			self.logy = kwargs['logy']
		except :
			self.logy = 0
			
		try :
			self.title = kwargs['title']
		except :
			self.title = ''
			
		try :
			self.ifvertical = kwargs['ifvertical']
		except :
			self.ifvertical = False
			
		try :
			self.axis = kwargs['axis']
			
			if axis not in [0, 1] : 
				raise OsirisSuiteError( 'ERROR: Plotter1DProjection currently only supports 2D input arrays') 

		except :
			self.axis = 0

		try :
			self.ifplotave = kwargs['ifplotave']
		except :
			self.ifplotave = False

		try : 
			self.ifplotmiddle = kwargs['ifplotmiddle']
		except :
			self.ifplotmiddle = False 

		try : 
			self.ifplotidx = kwargs['ifplotidx']
		except :
			self.ifplotidx = False

		try : 
			self.plotidx = kwargs['plotidx']
		except :
			self.plotidx = 0

		try : 
			self.iflegend = kwargs['iflegend']
		except :
			self.iflegend = False 
		
		try :
			self.xlabel = kwargs['xlabel']
		except :
			self.xlabel = ''

		try : 
			self.ylabel = kwargs['ylabel']
		except :
			self.ylabel = None

		try :
			self.aspect = kwargs['aspect']
		except :
			self.aspect = None
			
		try :
			self.ymin = kwargs['ymin']
		except :
			self.ymin = None 

		try :
			self.ymax = kwargs['ymax']
		except :
			self.ymax = None 

		try :
			self.transpose = kwargs[ 'transpose' ]
		except :
			self.transpose = False

		try :
			self.flipaxis = kwargs[ 'flipaxis' ]
		except :
			self.flipaxis = None
			

			
	def plot( self, ax, data, axes ) : 

		if data.ndim != 2 : 
			raise OsirisSuiteError( 'ERROR: Plotter1DProjection currently only supports 2D input arrays') 

		if self.transpose : 
			data = data.T 

		if self.flipaxis is not None  :
			data = np.flip( data, axis = self.flipaxis ) 
		
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

		if self.ifplotidx :

			if self.axis == 0 : 
				data_slice = data[:, self.plotidx ]
			else : 
				data_slice = data[ self.plotidx, :]

			label = 'x%d'%(1-self.axis + 1) + ' = ' + str(self.plotidx)
			ax.plot( xaxis, data_slice, label = label, c='g')

		if self.ymin is not None :
			ax.set_ylim( ymin = self.ymin ) 

		if self.ymax is not None :
			ax.set_ylim( ymax = self.ymax ) 

		if self.title : 
			ax.set_title( self.title ) 

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

	def __init__( 	self, multiple_data = False, **kwargs ) : 
		
		self.multiple_data = multiple_data 
		self.kwargs = kwargs 


	def plot( self, ax, data, axes ) : 

		plot_legend = False

		if 'plot_kwargs' in self.kwargs : 
			plot_kwargs = self.kwargs[ 'plot_kwargs' ]
		else : 
			plot_kwargs = {}

		# if multiple data are not supplied, package data into tuple
		# so we don't need to rewrite code below. 
		if not self.multiple_data : 
			data = (data,)
			axes = (axes,)
			plot_kwargs = (plot_kwargs,)

		for i in range( len( data ) ) : 

			# c = None if self.colors is None else self.colors[i]
			# linestyle = None if self.linestyles is None else self.linestyles[i]
			# label = None if self.labels is None else self.labels[i]

			xaxis = np.linspace( axes[i][0][0], axes[i][0][1], len( data[i]) )

			ax.plot( xaxis, data[i], **plot_kwargs[i] )

			if( 'label' in plot_kwargs[i] ) : 
				plot_legend = True 

		# ax.margins(x=0)
		# ax.margins(y=0)

		if 'xlabel' in self.kwargs : 
			ax.set_xlabel( self.kwargs[ 'xlabel' ])

		if 'ylabel' in self.kwargs : 
			ax.set_ylabel( self.kwargs[ 'ylabel' ] )

		if 'title' in self.kwargs : 
			ax.set_title( self.kwargs[ 'title' ] ) 

		if 'logy' in self.kwargs :
			if self.kwargs[ 'logy' ] : 
				ax.set_yscale( 'log' )

		if 'ymax' in self.kwargs : 
			ax.set_ylim( ymax = self.kwargs[ 'ymax' ] )

		if 'ymin' in self.kwargs : 
			ax.set_ylim( ymin = self.kwargs[ 'ymin' ] )

		if 'aspect' in self.kwargs : 
			xleft, xright = ax.get_xlim()
			ybottom, ytop = ax.get_ylim()
			ax.set_aspect(abs((xright-xleft)/(ybottom-ytop)) * self.kwargs['aspect'] )

		if plot_legend : 
			ax.legend( loc = 'best' )



def raw_osdata_TS_data_getter( osdata_leaf, ndump_fac = 1 ) : 

	return lambda index :  osdata_leaf.file_managers[ index // ndump_fac ].unpack()



# def slice_osdata_TS_data_getter( osdata_leaf, ndump_fac = 1 ) : 

# 	return lambda index :  osdata_leaf.file_managers[ index // ndump_fac ].unpack()



def raw_osdata_TS2D_plot_mgr( osdata_leaf, ndump_fac, modifier_function = None, **kwargs ) :
		
	data_getter = raw_osdata_TS_data_getter( osdata_leaf, ndump_fac )

	plotter = Plotter2D( **kwargs )	

	return PlotManager( data_getter, plotter, modifier_function )


def raw_osdata_TS1D_plot_mgr( 	osdata_leaf, modifier_function = None, 
								colors = None, linestyles = None, 
								labels = None,
								logy = 0, title = '',
								ndump_fac = 1,
								**kwargs ) : 
		
	data_getter = raw_osdata_TS_data_getter( osdata_leaf, ndump_fac )
	
	plotter = Plotter1D( multiple_data = False,
						 colors = colors, 
						 linestyles = linestyles, 
						 labels = labels,
					     logy = logy, 
					     title = title,
					     **kwargs )

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

	# note: used to use option -crf 25 (controls visual quality)
	command = 'ffmpeg -r %f -pattern_type sequence -i %s%%05d.png -vcodec libx264 -pix_fmt yuv420p -y %s' % ( 
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





def default_suptitle_function( osdata, timesteps, index ) : 

	# suptitle = ''

	suptitle = '\n' + os.path.basename( os.getcwd() )
	
	try : 
		timestep_metadata = osdata.input_deck.get_metadata( 'time_step')

		dt = timestep_metadata[ 'dt' ]
		ndump = timestep_metadata[ 'ndump' ]

		abs_time = timesteps[ index ] * dt * ndump

		suptitle += '\n%.2f$\\omega_\\mathrm{pe}^{-1}$' % abs_time

	except : 
		suptitle += '\nIdx=%d' % index 


	return suptitle 



def make_frame( index, osdata, timesteps,
				shape, plot_mgr_arr, 
				suptitle_function = default_suptitle_function, 
				figsize = None, subplots_adjust_kwargs = None, sharex = False ) : 

	N, M = shape 

	if figsize is None : 
		figsize = ( 15, 9 )

	fig, axarr = plt.subplots( * shape, sharex = sharex, 
			figsize = figsize, squeeze = 0 )

	if suptitle_function : 
		suptitle = suptitle_function( osdata, timesteps, index )
		fig.suptitle( suptitle )

	# make all plots 
	for i in range( N ) : 
		for j in range( M ) :
			
			plot_mgr = plot_mgr_arr[i][j]
			
			if plot_mgr is not None : 
				plot_mgr.plot( axarr[i,j], timesteps[index])
			
			else : 
				fig.delaxes( axarr[i,j] ) 

	if subplots_adjust_kwargs is not None : 
		fig.subplots_adjust( **subplots_adjust_kwargs )

	# plt.tight_layout(h_pad=1)

	return fig, axarr 






def make_TS_movie(  osdata, timesteps,
					plot_mgr_arr, 
					suptitle_function = default_suptitle_function, 
					figsize = None, subplots_adjust_kwargs = None,
					savedir = None, 
					frame_startup_function = None,
					frame_cleanup_function = None,
					global_modifier_function = None,
					nproc = 1, nframes = 20, duration = 5,
					print_progress = True,
					show_index = None,
					sharex = False,
					dpi = 400 ) : 
	
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

	timesteps = np.asarray( timesteps )

	spacing = int( len( timesteps ) / nframes ) # * ( timesteps[1] - timesteps[0])
	
	# indices = timesteps[ :: spacing ]
	indices = spacing * np.arange( nframes, dtype = int )

	try :
		abs_times = osdata.input_deck.get_abs_times( timesteps[ indices ] )
		print( 'INFO: plotting indices: ' + str( indices ) ) 
		print( 'INFO: corresponding abs times: ' + str( abs_times ) ) 

	except :
		...
		
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
								 suptitle_function, figsize, subplots_adjust_kwargs,
								 sharex )

		if global_modifier_function is not None : 
			global_modifier_function( fig, axarr ) 

		if frame_cleanup_function is not None : 
			frame_cleanup_function( index )

		path = frame_savedir + '/%05d' % i
		
		if show : 
			plt.savefig( path + '.pdf' ) 
			# plt.savefig( path, dpi = dpi ) 
			plt.show()

		else : 
			plt.savefig( path, dpi = dpi ) 
			plt.close() 


	if show : 
		handle_index( show_index )
		return 

	files = glob.glob( frame_savedir + '*')

	# only delete files if we aren't showing an index 
	for f in files:
		try:
			os.remove(f)
		except : 
			print("Error deleting file: %s " % (f ))

	print( 'nproc: ', nproc ) 

	if( nproc > 1 ) : 
		pool = pathos.multiprocessing.ProcessingPool( nproc ) 

		pool.map( handle_index, range( len( indices ) ) )	

		pool.close()

	else : 
		for i in range( len( indices) ) : 
			handle_index( i ) 
	
	movie_path = ( savedir 
		+ os.path.basename( os.path.dirname( savedir ) ) 
		+ '.mp4' ) 

	print( 'Saving movie...' )

	ffmpeg_combine( frame_savedir, movie_path, duration )



