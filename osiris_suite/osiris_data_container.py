import numpy as np
import os 
import glob
import sys
import h5py
import collections 
from pprint import pprint  
import re 


from .helper_classes import AttrDict, RecursiveAttrDict





class OsirisSuiteError( Exception ) : 
	... 



MS_PREFIX = '/MS'



# class OsirisData( h5py.File ) : 




class OsirisDataContainer( object ) : 
	'''

	'''


	def __init__( self, data_path = None, load_whole_file = False,
				load_empty_directories = False,
				silent = False , index_by_timestep = False ) : 
		'''
			data_path: path to parent directory containing all OSIRIS data (i.e. the directory)
				containing the OSIRIS output directory MS).

			load_whole_file: if nonzero, this will make the entire hdf5 get loaded for each file
				instead of returning a handle to the hdf5 file accessed at the data. 
				this does not add much overhead, but if you are only planning to access the data
				and none of the metadata you don't need to access the whole file. i include the option
				because it is occasionally useful to inspect the other data.  

			load_empty_directories: if True, will assume that any empty directories were supposed to contain 
				hdf5 files, and hence will create a stub for these. if False, the directories will be ignored.

			silent: if True, will prevent debug info from being printed. 

			index_by_timestep: if True, data is stored with index = t_0, ..., t_N where t_i are the N timesteps 
				output for this data in the simulation. if False, the data is stored with index = 0 ... N independent 
				of the timesteps. in either case the timesteps variable stores the values t_0 ... t_N.
		'''
	
		if not os.path.exists( data_path ) : 
			raise OSError( 'Error: the specified path does not exist: %s' % data_path )

		self.data_path = data_path 
		self.load_whole_file = load_whole_file
		self.load_empty_directories = load_empty_directories
		self.silent = silent 
		self.index_by_timestep = index_by_timestep

		# data structures
		self.data = RecursiveAttrDict() 
		self.derived_data = AttrDict() 
		self.has_empty_dir = False

		# track all the indices that have data loaded 
		# self.loaded_indices = set()
		# self._keys_at_prefix = {} 



	def load_indices( self, indices = None, timesteps = None, keys = None, prune = 1 ) : 
		
		self.load_ms( indices, timesteps, keys ) 
		self.load_timings()

		if self.has_empty_dir : 
			if not self.silent : 
				print( 'INFO: pruning empty data branches' )
			self.data.prune()	






	def unload_indices( self, indices = None, timesteps = None, keys = None ) : 
		... 



	def load_ms( self,  indices = None, timesteps = None, keys = None ) : 
		ms_path = self.data_path + MS_PREFIX 
		# pprint( list( os.walk (ms_path)) )

		if not os.path.exists( ms_path ) : 
			raise OSError( 'ERROR: the MS directory does not exist: %s' % ms_path)

		self.data.ms = AttrDict() 
		self.recursively_load_dir( self.data.ms, ms_path )




	def recursively_load_dir( self, parent_dict, directory ) : 

		curpath, subdir_names, files = next( os.walk( directory ) ) 

		if len( subdir_names ) > 0 : 
			for subdir_name in subdir_names : 
				# basename = os.path.basename( os.path.normpath( subdir ) ).lower() 
				# parent_dict[ basename ] = AttrDict() 
				subdir = os.path.join( directory, subdir_name )
				key = subdir_name.lower() 
				parent_dict[ key ] = AttrDict() 
				self.recursively_load_dir( parent_dict[ key ], subdir )

		# otherwise load files 
		else : 
			if len( files ) > 0 : 
				self.load_h5_files( parent_dict, directory ) 

			else : 	
				self.has_empty_dir = True
				if not self.silent : 
					print( 'WARNING: found empty directory: %s' % directory )

				if self.load_empty_directories : 
					self.load_h5_files( parent_dict, directory )

				# else : 
				# 	curkey = 
				# 	del self.parent_dict[ ] 



	def load_h5_files( self, parent_dict, directory, slice_ = None ) : 

		files = sorted( glob.glob( directory + '/*.h5' ) )
		timesteps = [ get_timestep( fname ) for fname in files ]

		varname = os.path.basename( os.path.normpath( directory ) )

		parent_dict[ 'timesteps' ] = timesteps 

		for i in range( len( files ) ) : 
			
			data = h5py.File( files[i], 'r')

			if not self.load_whole_file : 
				data = data[ varname ]
		
				# apply a slice if requested	
				if slice_ is not None : 
					data = data[ slice_ ] 

			# add this data to the parent dictionary 
			if self.index_by_timestep :
				parent_dict[ timesteps[ i ] ] = data 
			else : 
				parent_dict[ i ] = data 


		# print( 'in directory: %s' % directory )
		# print( 'files: ' + str( files ) )



	def load_timings( self ) : 
		self.timings = None 



	def __str__( self ) : 
		return str( self.data ) 


		


		
			
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

						







