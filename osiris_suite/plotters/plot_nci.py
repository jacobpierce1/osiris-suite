from osiris_suite import OsirisDataContainer
import osiris_suite.utils as utils 
import matplotlib.pyplot as plt 
import colorcet 
from pprint import pprint 
import numpy as np 
import os 



def plot_nci( data_path, timestep ) : 


	osdata = OsirisDataContainer( data_path, load_whole_file = True )

	osdata.load_ms( indices = [ -1 ] )   
	osdata.load_hist() 

	print( osdata ) 

	print( osdata.data.ms.fld.b1 )

	data = osdata.data.ms.fld.b1.data[ timestep ]
	utils.scan_hdf5( data )
	print( data['b1'].shape )

	fig, axarr = plt.subplots( 2, 4, figsize = ( 16, 6 ) ) 

	fig.suptitle( os.path.basename( os.getcwd() ) )


	axarr[0,0].set_title( 'Total Energy vs. Time' ) 
	axarr[0,0].set_ylabel( 'Energy (normalized units)')
	axarr[0,0].set_xlabel( 'T $[\omega_\mathrm{pe}^{-1}]$')
	# axarr[1].set_title( '$U_{E2}$ vs. Time')

	timesteps = osdata.data.hist.fld_ene.Iter
	times = osdata.data.hist.fld_ene.Time

	keys = [ 'E1', 'E2', 'E3' ]
	colors = 'rgb'

	# for i in range( 3 ) : 
	for j in range(3) : 
		times = osdata.data.hist.fld_ene[ 'Time' ]
		data = osdata.data.hist.fld_ene[ keys[j] ]
		axarr[0,0].plot(  times, data, c = colors[j], label = keys[j] )


	keys = [ 'par01_ene', 'par02_ene' ]

	labels = ['Electron KE', 'Ion KE' ]
	colors = 'km'

	for j in range(1) : 
	# for j in range( len( keys )) : 
		times = osdata.data.hist[ keys[j] ][ 'Time' ]
		data = osdata.data.hist[ keys[j] ][  'KinEnergy' ]
		axarr[0,0].plot( times, data, c = colors[j], linestyle = '--', label = labels[j] ) 


	# for j in range( len( keys ) ) : 

	# 	axarr[0].plot( E_mean[j,:], c = colors[j], label = keys[j] )
	# 	axarr[1].plot( E_std[j,:], c = colors[j], label = keys[j] )
	for k in range(2) : 
		axarr[0,k].legend()
		axarr[0,k].ticklabel_format( style = 'sci')



	axarr[0,0].set_yscale( 'log' )


	keys = [ 'e1', 'e2', 'e3' ]

	for j in range( len( keys ) ) : 
		
		key = keys[j]

		# print( osdata.data.ms.fld[key] )
		# print( osdata.data.ms.fld[key][timestep].keys())

		# utils.scan_hdf5(osdata.data.ms.fld[key][timestep] )

		# axis1 = np.array( osdata.data.ms.fld[ key ][ timestep ]['AXIS'][ 'AXIS1' ] ) 
		# axis2 = np.array( osdata.data.ms.fld[ key ][ timestep ]['AXIS'][ 'AXIS2' ] ) 
		
		# skip data if not available 
		try : 
			data = np.array( osdata.data.ms.fld[ key ].data[ timestep ][ key ] ) 
		except : 
			continue

		# apply fft 
		fft = np.fft.fftn( data ) 
		fft = np.abs( fft ) 

		# print( axis1 ) 

		k1_axis = 2 * np.pi * np.fft.fftfreq( data.shape[0] )
		k2_axis = 2 * np.pi * np.fft.fftfreq( data.shape[1] )

		k1_axis = np.fft.fftshift( k1_axis )
		k2_axis = np.fft.fftshift( k2_axis )
		fft = np.fft.fftshift( fft ) 
		
		ax = axarr[ 0, j + 1 ]

		ax.pcolormesh( k1_axis, k2_axis, fft.T, cmap = colorcet.m_CET_L16 ) 

		ax.set_title( 'FFT( ' + keys[j] + ' )' )
		ax.set_xlabel( 'k_1 (direction of drift)' )
		ax.set_ylabel( 'k_2' )


	key = 'dens'
	data = np.array( osdata.data.ms.density.electrons.charge.data[ timestep ][ 'charge' ] )

	# print( data ) 

	# utils.scan_hdf5( data) 

	
	ax = axarr[1,0]
	im = ax.pcolormesh( data )
	fig.colorbar( im, ax = ax, cmap = colorcet.m_CET_L16 )

	plt.show() 