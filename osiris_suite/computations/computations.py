from osiris_suite import OsirisDataContainer 
import numpy as np 


def compute_fft_2d( data ) : 
	
	fft = np.fft.fftn( data ) 
	fft = np.abs( fft ) 

	# k2_axis = np.fft.fftfreq( data.shape[0] )
	# k1_axis = np.fft.fftfreq( data.shape[1] )

	# k1_axis = np.fft.fftshift( k1_axis )
	# k2_axis = np.fft.fftshift( k2_axis )
	
	fft = np.fft.fftshift( fft ) 

	# return fft, ( k1_axis, k2_axis )
	return fft, ( [-0.5, 0.5], [-0.5, 0.5] )



def compute_lorentz_transformation( osdata, gamma, 
								e_leaves, b_leaves, j_leaves,
								phase_space_leaves, 
								load = 1, save = 0 ) : 

	'''
		apply lorentz boost along the direction of the first leaf
		the leaves must be specified in a right-handed coordinate system
		e.g. ( e3, e1, e2 ) would transform along z direction in cartesian
		coordinates 
	'''

	boosted_data = OsirisDataContainer() 

	# check if the boost gamma is compatible with the unboosted mesh



class Q3DFieldComputationManager( object ) : 

	def __init__( self, osdata, key ) : 

		self.osdata = osdata
		self.key = key 

		self.gather_leaves() 


	def gather_leaves( self ) : 

		leaves = [] 

		branch = self.osdata.data.ms.fld
		
		m = 0 
		while ( 1 ) : 
			key = 'mode_%d_re' % m
			
			if key not in branch :
				break  

			# mode m is present. load the leaves. 
			leaves.append( [ None, None ] )

			fld_key = '%s_cyl_m' % self.key
			leaves[m][0] = branch[ key ][ fld_key ] 

			key = 'mode_%d_im' % m

			if m > 0 : 
				leaves[m][1] = branch[ key ][ fld_key ] 

			# no data for the im0 mode 
			# else : 
			# 	leaves[m][1] = None

			m += 1 

		self.leaves = leaves
		self.num_leaves = m 


	def compute_xz_projection( self, index ) : 	

		for m in range( self.num_leaves ) : 

			if m == 0 : 
				data, axes = self.leaves[m][0].file_managers[ index ].unpack()
				ret = data 

			else : 
				data, axes = self.leaves[m][0].file_managers[ index ].unpack()
				ret += data		

		return ret, axes



	@classmethod
	def decompose_fields( cls, fields ) : 

		...

