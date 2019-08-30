import numpy as np
import os 
import glob
import sys
import h5py
import collections 


#class OsirisSuiteError( Exception ) : 
# 	... 



MESH_DIR_PREFIX = '/MS'



class OsirisDataContainer( object ) : 

	def __init__( self, data_path ) : 

		'''
		load all data within path 

		'''

		if not os.path.isdir( data_path ) : 
			raise IOError( 'ERROR: %s is not a directory' % data_path )


		self.mesh_data = {} 
		self.particle_data = {} 
		self.tracking_data = {} 


		print( list( os.walk( data_path ) ) )

