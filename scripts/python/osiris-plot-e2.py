import numpy as np 
import os 
import sys 
import matplotlib.pyplot as plt 
import colorcet
from scipy.interpolate import interp2d
import argparse 

from mpl_toolkits.axes_grid1 import make_axes_locatable


from osiris_suite import OsirisDataContainer 


parser = argparse.ArgumentParser( description = 'Plot e2.' )


parser.add_argument( '--data_path', '-d', dest = 'data_path', 
			type = str, help = 'parent directory of data' )   # parent directory of data

parser.add_argument( '--res', '-r', type = int, dest = 'res',
			default = 1, help = 'interpolation resolution' )   # interpolation resolution 

parser.add_argument( '--index', '-i', dest = 'index',
				type = int, default = 1, help = 'index to plot' ) 

args = parser.parse_args()

# print( args )

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

	e2_interp_f = interp2d( x, y, data, kind = 'cubic' )

	xnew = np.linspace( 0, data.shape[1], res * data.shape[1] )
	ynew = np.linspace( 0, data.shape[0], res * data.shape[0] )

	interpolated = e2_interp_f( xnew, ynew )
	return ( xnew, ynew, interpolated ) 




print( data_path ) 

osdata = OsirisDataContainer( data_path )

osdata.load_indices()


timesteps = osdata.data.ms.fld.e2.timesteps
timestep = timesteps[ 1 ]
e2 = osdata.data.ms.fld.e2[ timestep ]

if res > 1 : 
	xnew, ynew, e2_interp = interpolate_2d_data( e2, res = res )
else : 
	e2_interp = e2


print( timesteps )


fig, ax = plt.subplots( figsize = ( 6, 6 ) ) 

im = ax.pcolormesh( e2_interp, cmap = colorcet.m_fire )
make_colorbar( im ) 

ax.set_aspect( 'auto' )

plt.show() 