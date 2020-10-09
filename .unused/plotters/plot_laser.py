from osiris_suite import OsirisDataContainer
import osiris_suite.utils as utils 
import colorcet 
from pprint import pprint 
import numpy as np 
import os 

import matplotlib
# matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import matplotlib.pyplot as plt 

import glob 
import imageio
from PIL import Image



def ffmpeg_combine( plotdir, movie_name ):
    os.system( 'ffmpeg -r 4 -i %s%%03d.png -vcodec mpeg4 -y %s' % ( plotdir, movie_name ) )



def gif_combine( plotdir, gif_name ) : 

	# filenames = os.listdir( plotdir ) 
	filenames = glob.glob( plotdir + '*' )

	print( plotdir )
	print( filenames )

	# images = []
	
	# for filename in filenames:

	# 	path = plotdir + filename 
    
	# 	images.append( imageio.imread( path, plugin = 'matplotlib' ))
	
	# imageio.mimsave( gif_name, images )

	frames = [] 

	for f in filenames :
		# path = plotdir + f
		print( f ) 
		new_frame = Image.open( f )
		frames.append( new_frame )
 
	# Save into a GIF file that loops forever
	frames[0].save( gif_name, format='GIF',
            	  	 append_images=frames[1:],
	           	    save_all=True,
	           	    duration=300, loop=0)


def plot_laser( data_path, savedir = None, N_frames = 10, timestep = None ) : 

	if savedir is None : 
		savedir = data_path + '/plots/summary/'

	os.makedirs( savedir, exist_ok = 1 )

	osdata = OsirisDataContainer( data_path, load_whole_file = True )

	osdata.load_hist() 

	keys = [ 'e1', 'e2', 'e3', 'dens' ]

	# timesteps = osdata.data.hist.fld_ene.Iter.astype( int )
	# times = osdata.data.hist.fld_ene.Time


	

	# osdata.load_ms( indices = frame_timesteps ) 
	osdata.load_ms() 

	timesteps = np.array( osdata.data.ms.fld.e1.timesteps, dtype = int ) 
	indices = timesteps / timesteps[1] 
	indices = indices.astype( int )

	print (osdata.data.ms.fld.e1)

	spacing = len( indices  ) // N_frames


	frame_indices = indices[ :: spacing ]
	# frame_times = times[ :: spacing ] 


	print( frame_indices ) 


	# for j in range( len( keys ) ) : 
	# 	key = keys[j]
	# 	plotdir = savedir + '/' + key + '/'
	# 	os.makedirs( plotdir, exist_ok = 1 ) 

	for i in range( len( frame_indices ) ) : 

		# continue

		timestep = frame_indices[i]
		
		axarr_shape  = (2,2)

		fig, axarr = plt.subplots( * axarr_shape, figsize = (10,10) )

		print( timestep ) 

		for j in range( len( keys ) ) : 
			
			ax_index = np.unravel_index( j, axarr_shape ) 

			ax = axarr[ ax_index ]

			key = keys[j]

			
			if key == 'dens' : 
				continue 
				# data = np.array( osdata.data.ms.density.electrons.charge.data[ timestep ][ 'charge' ] )

			# try : 
			# 	data = np.array( osdata.data.ms.fld[ key ].data[ timestep ][ key ] ) 
			# except : 
			# 	continue
			else : 	
				data = np.array( osdata.data.ms.fld[ key ].data[ timestep ][ key ] ) 

			im = ax.pcolormesh( data )
			fig.colorbar( im, ax = ax, cmap = colorcet.m_CET_D1A )
			
			# plt.show() 

			plt.savefig( savedir + '%03d.png' % timestep, dpi = 400 ) 

		# video_path = plotdir + key + '.mp4'
		# ffmpeg_combine( plotdir )

	gif_path = savedir + 'summary.gif'
	gif_combine( savedir, gif_path )

