from .osiris_data_container import OsirisDataContainer 



def apply_lorentz_transformation( osdata, gamma, 
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
