from osiris_suite import OsirisDataContainer
import osiris_suite.utils as utils 


from pprint import pprint 

# data_path = '../test-data/test-data-2d'
data_path = '../test-data/test-data-PA'

osdata = OsirisDataContainer( data_path, 
				load_whole_file = True )

osdata.load_indices()  

# print( osdata )

# print( a.data.ms.boosted.keys() )

# print( osdata.data.ms.boosted.e1 )


e1 = osdata.data.ms.fld.e1

# it's a bunch of files
pprint( e1 ) 

utils.scan_hdf5( e1[0] )

print( '\nindex 0' )  
print( e1[0][ 'AXIS' ][ 'AXIS1' ][:] )
print( e1[0][ 'AXIS' ][ 'AXIS2' ][:] )

print( '\nindex 1' )
print( e1[1][ 'AXIS' ][ 'AXIS1' ][:] )
print( e1[1][ 'AXIS' ][ 'AXIS2' ][:] )


# print( e1[0][ 'AXIS' ].keys() ) 

# print( )




