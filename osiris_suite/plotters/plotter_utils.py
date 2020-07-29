
import glob 
import imageio
from PIL import Image


def ffmpeg_combine( plotdir, movie_name, duration ):
    os.system( 'ffmpeg -r 4 -i %s%%03d.png -vcodec mpeg4 -y %s' % ( plotdir, movie_name ) )



def gif_combine( plotdir, gif_name, duration ) : 

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



def plot_2d_raw( fig, ax, osdata_leaf, index, cmap, title ) : 

	data_mgr = osdata_leaf.file_managers[ index ]

	data_mgr.load() 
	data = data_mgr.data 
	axes = data_mgr.axes

	# print( axes ) 

	# extent = [ axes[i][j] for i in [0,1] for j in [0,1]  ]

	# print( extent )

	im = ax.imshow( data, cmap = cmap, interpolation = 'bilinear', 
					origin = 'lower' ) # , extent = extent )

	fig.colorbar( im, ax = ax )

	ax.set_title( title )

	data_mgr.unload() 
