import h5py

recursive = 1 
tab_step = 2 

def scan_hdf5( opened_h5file ) : 
	scan_node( opened_h5file )


def scan_node(g, tabs=0):
	
	print(' ' * tabs, g.name)
	
	for k, v in g.items():

		if isinstance(v, h5py.Dataset):
			print(' ' * tabs + ' ' * tab_step + ' -', v.name)

		elif isinstance(v, h5py.Group) and recursive:
			scan_node(v, tabs=tabs + tab_step)