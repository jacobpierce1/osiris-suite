import numpy as np 
import os 
import sys 
import matplotlib.pyplot as plt 
import colorcet
from scipy.interpolate import interp2d
import argparse 

from mpl_toolkits.axes_grid1 import make_axes_locatable


from osiris_suite import OsirisDataContainer 


parser = argparse.ArgumentParser( description = 'Plot data.' )

parser.add_argument( dest = 'quantity', type  = str, help = 'quantity to plot', nargs = 1 )

parser.add_argument( '--data_path', '-d', dest = 'data_path', 
			type = str, help = 'parent directory of data' )   # parent directory of data

parser.add_argument( '--res', '-r', type = int, dest = 'res',
			default = 1, help = 'interpolation resolution' )   # interpolation resolution 

parser.add_argument( '--index', '-i', dest = 'index',
				type = int, default = 0, help = 'index to plot' ) 

args = parser.parse_args()

# print( args )

quantity = args.quantity[0]
data_path = args.data_path 
res = args.res
index = args.index 

if data_path is None : 
	data_path = os.getcwd()

# sys.exit( 0 )



import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


def make_colorbar( mappable ):
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    return fig.colorbar(mappable, cax=cax)



def interpolate_2d_data( data, res = 10 ) : 

	x = np.arange( data.shape[1] )
	y = np.arange( data.shape[0] )

	data_interp_f = interp2d( x, y, data, kind = 'cubic' )

	xnew = np.linspace( 0, data.shape[1], res * data.shape[1] )
	ynew = np.linspace( 0, data.shape[0], res * data.shape[0] )

	interpolated = data_interp_f( xnew, ynew )
	return ( xnew, ynew, interpolated ) 




print( data_path ) 

osdata = OsirisDataContainer( data_path )

osdata.load_indices()


# timestep = timesteps[ index ]
print( 'quantity: ' + quantity )

data = osdata.find_subtree( quantity )

timesteps = data.timesteps
data = data[ index ] 

print( timesteps )


if res > 1 : 
	xnew, ynew, data_interp = interpolate_2d_data( data, res = res )
else : 
	data_interp = data




# fig, ax = plt.subplots( figsize = ( 8, 8 ) ) 

ax = plt.axes() 

cmap = colorcet.m_CET_D8

im = ax.pcolormesh( data_interp, cmap = cmap )
make_colorbar( im ) 

ax.set_aspect( 'auto' )

plt.show() 