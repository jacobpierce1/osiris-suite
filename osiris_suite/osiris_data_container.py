import numpy as np
import os 
import glob
import sys
import h5py
import collections 
from pprint import pprint  
import re 


from .helper_classes import RecursiveAttrDict, AttrDict





class OsirisSuiteError( Exception ) : 
	... 



MS_PREFIX = '/MS'



# class OsirisData( h5py.File ) : 




class OsirisDataContainer( object ) : 

	def __init__( self, data_path = None  ) : 
		
		if not os.path.exists( data_path ) : 
			raise OSError( 'Error: the specified path does not exist: %s' % data_path )

		self.data_path = data_path 

		self.data = AttrDict() 
		self.derived_data = AttrDict() 

		# track all the indices that have data loaded 
		# self.loaded_indices = set()
		# self._keys_at_prefix = {} 



	def load_indices( self, indices = None, timesteps = None, keys = None ) : 
		
		self.load_ms( indices, timesteps, keys ) 
		self.load_timings()



	def unload_indices( self, indices = None, timesteps = None, keys = None ) : 
		... 


	def load_ms( self,  indices = None, timesteps = None, keys = None ) : 
		ms_path = self.data_path + MS_PREFIX 
		# pprint( list( os.walk (ms_path)) )

		self.data.ms = AttrDict() 
		self.recursively_load_dir( self.data.ms, ms_path )



	def recursively_load_dir( self, parent_dict, directory ) : 

		# for parent, dirs, files in os.walk( directory ) : 

		#	parent_dict[ ]

			# key = os.ms_path.normpath( os.path.basename( 

		# subdirs = os.listdir( directory ) 
		curpath, subdir_names, files = next( os.walk( directory ) ) 


		# print( subdir_names ) 

		# load all directories if possible 
		if len( subdir_names ) > 0 : 
			for subdir_name in subdir_names : 
				# basename = os.path.basename( os.path.normpath( subdir ) ).lower() 
				# parent_dict[ basename ] = AttrDict() 
				subdir = os.path.join( directory, subdir_name )
				key = subdir_name.lower() 
				parent_dict[ key ] = AttrDict() 
				self.recursively_load_dir( parent_dict[ key ], subdir )

		# otherwise load files 
		elif len( files ) > 0 : 
			self.load_h5_files( parent_dict, directory ) 

		else : 
			print( 'WARNING: found empty directory: %s' % directory )



	def load_h5_files( self, parent_dict, directory, slice_ = None ) : 

		files = sorted( glob.glob( directory + '/*.h5' ) )
		timesteps = [ get_timestep( fname ) for fname in files ]

		varname = os.path.basename( os.path.normpath( directory ) )

		parent_dict[ 'timesteps' ] = timesteps 

		for i in range( len( files ) ) : 
			
			data = h5py.File( files[i], 'r')[ varname ]
			
			if slice_ is not None : 
				data = data[ slice_ ] 

			parent_dict[ timesteps[i] ] = data 

		# print( 'in directory: %s' % directory )
		# print( 'files: ' + str( files ) )



	def load_timings( self ) : 
		self.timings = None 



	def __str__( self ) : 

		ret = '' 

		ret += attrdict2str( self.data, 0, '' )

		return ret


		
	
def attrdict2str( attrdict, depth, accumulated_str ) : 
	
	#accumulated_str = ''

	# print( attrdict.keys() )

	try : 
		keys = sorted( attrdict.keys() )
	except : 
		return ''

	for key in sorted( attrdict.keys() ):
		
		val = attrdict[ key ]

		if isinstance( val, AttrDict ) : 
			# print( k )
			currline = '---- ' * depth + '%s\n' % key
			# print( currline ) 
			

			accumulated_str += currline + attrdict2str( val, depth + 1, accumulated_str )

	return accumulated_str


	 
		
			
# helper functions
def idx_to_str( idx ) :
	return '%06d' % idx 

def get_timestep( os_h5_fname ) : 
	left = os_h5_fname.rfind( '-' ) + 1 
	right = os_h5_fname.rfind( '.' )

	timestep = int( os_h5_fname[ left : right ] )
	# print( timestep )
	return timestep 



def get_num_files( output_path ) :	
	num_files = len( glob.glob( output_path ) ) 
	return num_files

								   





