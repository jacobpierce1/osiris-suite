from osiris_suite import OsirisDataContainer 

test_data_path = '../test-data/test-data-2d'


a = OsirisDataContainer( test_data_path )

a.load_indices()  

# print( a.keys() )

print( a )