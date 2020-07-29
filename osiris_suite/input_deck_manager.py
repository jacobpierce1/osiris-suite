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


	# read an input deck 
	def read( self, path = None ) : 

		if path is None : 
			path = self.path 

		with open( self.path ) as f : 
			text = f.read()

		self.keys = []
		self.metadata = []

		# remove comments 
		text = re.sub( r'!.*\n', '', text )

		# remove newlines 
		text = text.replace( '\n', '' )			

		matches = re.findall( r'(.*?){(.*?)}', text )

		self.keys = [ x[0] for x in matches ] 

		# print( self.keys ) 

		for key, metadata in matches : 
						
			cur_metadata = collections.OrderedDict()
			self.metadata.append( cur_metadata )

			metadata_split = re.findall( r'(.*?)=([^=(]*),', metadata )

			for metadata_key, metadata_val in metadata_split : 

				metadata_key = metadata_key.strip()
				metadata_val = metadata_val.strip() 

				metadata_val_split = metadata_val.split( ',' )

				is_arr = ( len( metadata_val_split ) > 1 ) 

				# in either case, try to store it as a float.
				# if unsuccessful, keep the string version
				# type casting of the key is not currently supported
				# because of the challenges this introduces 
				# in conjuction with how rarely this would be useful

				if is_arr : 
					try : 
						metadata_val = np.array( metadata_val_split, dtype = float )
					except : 
						metadata_val = np.array( metadata_val_split, dtype = str )

				else : 
					try : 
						metadata_val = float( metadata_val )
					except : 
						... 

				cur_metadata[ metadata_key ] = metadata_val 



	# write the data into an input deck
	def write( self, path ) : 

		... 


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



	def __str__( self ) : 

		n = len( self.keys ) 

		s = ''

		for i in range( n ) : 

			s += self.keys[i] 
			s += '\n'

			for key, val in self.metadata[i].items() : 

				s += '\t%s = %s\n' % ( str(key), str(val) )

			s += '\n\n'

		return s 




def string_to_array( string ) : 

	...


def array_to_string( arr ) : 

	... 
