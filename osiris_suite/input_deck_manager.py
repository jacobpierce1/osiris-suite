import os 
import re 
import collections
import numpy as np 

from .helper_classes import OsirisSuiteError


class InputDeckManager( object ) : 

	def __init__( self, path = None ) : 

		self.path = path

		# list of keys, e.g. simulation, node_conf, etc.
		self.keys = []
		
		# list of OrderedDicts containing the corresponding metadata 
		# for each entry of self.keys 
		self.metadata = [] 

		if path is not None : 
			self.read() 


	def copy( self ) : 
		copy = type( self )()
		copy.keys = self.keys.copy()
		copy.metadata = [] # [ x.copy() for x in self.metadata ]

		# the numpy arrays have to be separately copied
		for odict in self.metadata :
			odict_copy = collections.OrderedDict()  
			for key, val in odict.items() :
				if isinstance( val, np.ndarray ) : 			
					odict_copy[key] = val.copy() 
				else : 
					odict_copy[key] = val 
			copy.metadata.append( odict_copy )

		return copy 


	# read an input deck 
	def read( self, path = None ) : 

		if path is None : 
			path = self.path 

		try : 
			with open( self.path ) as f : 
				text = f.read()
		except :
			raise OsirisSuiteError( 'ERROR: unable to open input deck: %s' % self.path )

		self.keys = []
		self.metadata = []

		# remove comments 
		text = re.sub( r'!.*\n', '', text )

		# remove newlines 
		text = text.replace( '\n', '' )			

		matches = re.findall( r'(.*?){(.*?)}', text )

		self.keys = [ x[0].strip() for x in matches ] 

		# print( self.keys ) 

		for key, metadata in matches : 
						
			cur_metadata = collections.OrderedDict()
			self.metadata.append( cur_metadata )

			metadata_split = re.findall( r'(.*?)=([^=(]*),', metadata )

			for metadata_key, metadata_val in metadata_split : 

				metadata_key = metadata_key.strip()
				metadata_val = metadata_val.strip() 

				# first split into quote pairs -- we use this for if it's a string 
				metadata_val_split = re.findall( r'(\".+?\")', metadata_val )

				# no match: is not string, split by commas instead.  
				if len(metadata_val_split ) == 0 : 
	
					metadata_val_split = metadata_val.split( ',' )

				# print( metadata_val_split )

				is_arr = ( len( metadata_val_split ) > 1 ) 

				# in either case, try to store it as a float.
				# if unsuccessful, keep the string version
				# type casting of the key is not currently supported
				# because of the challenges this introduces 
				# in conjuction with how rarely this would be useful

				bool_strs = [ '.true.', '.false.' ]

				if is_arr : 

					if metadata_val_split[0] in bool_strs :

						true_mask = np.array( [ b.strip() == '.true.' for b in metadata_val_split ] )
						
						metadata_val = np.zeros_like( metadata_val_split, dtype = bool )
						metadata_val[ true_mask ] = True
						metadata_val[ ~true_mask ] = False

					else : 
						# try int array
						try : 
							metadata_val = np.array( metadata_val_split, dtype = int )
						except : 
							# try float array
							try : 
								metadata_val = np.array( metadata_val_split, dtype = float )
							# try string array
							except : 
								for i in range( len( metadata_val_split)) : 
									metadata_val_split[i] = metadata_val_split[i].strip( ' ' ).replace( '"', '' )
								metadata_val = np.array( metadata_val_split, dtype = str )

				else : 

					if metadata_val in bool_strs : 
						metadata_val = True if (metadata_val == '.true.' ) else False

					else : 
						# try int 
						try : 
							metadata_val = int( metadata_val )
						except :
							# try float
							try :
								metadata_val = float( metadata_val )
							# last case: do nothing since it's already a string  
							except : 
								metadata_val = metadata_val.replace( '"', '' )
							
				cur_metadata[ metadata_key ] = metadata_val 

				# print( metadata_key ) 
				# print( metadata_val ) 


	# write the data into an input deck
	def write( self, path ) : 

		with open( path, 'w' ) as f : 
			f.write( str( self ) )



	def get_metadata( self, key, occurrence = 0, truncate_strings = 1 ) : 

		'''
		trunacte_strings = 1 will remove the double quotes from 
				strings in the input deck when fetching metadata 
		'''

		if key not in self.keys :
			raise OsirisSuiteError( 
				'ERROR: key is not in input deck: %s' % str(key) )

		# get indices which match key 
		indices = [ i for i, x in enumerate( self.keys ) if x == key ]

		idx = indices[ occurrence ] 

		return self.metadata[ idx ] 



	def __getitem__( self, attr_occurrence_val_tuple ) :

		x = attr_occurrence_val_tuple

		if isinstance( x, tuple ) : 
			attr = x[0] 

			if len( x ) > 1 : 
				occurrence = x[1] 
			else : 
				occurrence = 0 

			if len(x) > 2 : 
				val = x[2] 
			else : 
				val = None 

		else : 
			attr = x
			occurrence = 0
			val = None

		metadata = self.get_metadata( attr, occurrence )

		if val is None : 
			return metadata

		else : 
			return metadata[ val ]



	def __setitem__( self, attr_and_occurrence, val ) : 

		if isinstance( attr_and_occurrence, tuple ) : 
			attr, occurrence = attr_and_occurrence
		else : 
			attr = attr_and_occurrence
			occurrence = 0

		if key not in self.keys :
			raise OsirisSuiteError( 
				'ERROR: key is not in input deck: %s' % str(key) )

		# get indices which match key 
		indices = [ i for i, x in enumerate( self.keys ) if x == key ]

		idx = indices[ occurrence ] 

		self.metadata[ idx ] = val 



	def __str__( self ) : 

		n = len( self.keys ) 

		s = ''

		for i in range( n ) : 

			s += self.keys[i] 
			s += '\n{\n'

			for key, val in self.metadata[i].items() : 

				if isinstance( val, np.ndarray ) : 
					val_str = array_to_string( val )
				else : 
					val_str = val_to_string( val ) 

				s += '  %s = %s\n' % ( str(key), val_str )

			s += '}'

			s += '\n\n'

		return s 


	def num_occurrences( self, key ) : 

		# get indices which match key 
		indices = [ i for i, x in enumerate( self.keys ) if x == key ]

		return len( indices ) 


	# utilities 
	def get_abs_times( self, indices ) : 
		
		dt = self[ 'time_step' ][ 'dt' ]
		try :
			ndump = self[ 'time_step' ][ 'ndump' ]
			return dt * ndump * np.asarray( indices ) 
		except : 
			return np.asarray( indices ) 


	def insert( self, idx, key ) : 

		self.keys.insert( idx, key ) 
		self.metadata.insert( idx, collections.OrderedDict() )


# def string_to_array( string ) : 

# 	...


def array_to_string( arr ) : 

	ret = '' 

	for x in arr : 
		ret += val_to_string( x ) 
		ret += ' '
		# ret += ','

	return ret 



def val_to_string( val ) : 

	if isinstance( val, (bool, np.bool_ ) ) : 
		ret = '.true.' if val else '.false.'

	elif isinstance( val, str ) : 
		ret = '"' + str( val ) + '"'

	else : 
		ret = str( val ) 

	ret += ','

	return ret 
