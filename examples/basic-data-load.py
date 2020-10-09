from osiris_suite import OsirisDataContainer

data_path = './test-data/test-data-2D/'
input_deck_path = data_path + 'input.os'

# input deck path is not necessary to specify, but for 
# most applications having the input deck data in memory will
# be useful. 
osdata = OsirisDataContainer( data_path, input_deck_path = input_deck_path )

# the above OsirisDataContainer loads the directory structure but 
# does not load any of the data. view the data hierarchy here: 
print( 'INFO: printing osdata')
print( osdata ) 

# how to unpack data indexed at timesteps (i.e. in the MS directory):
e1 = osdata.data.ms.fld.e1
timesteps = e1.timesteps 

print( 'INFO: available timesteps:')
print( timesteps ) 

# let's pull out data at this index:
# get handle to class wrapping corresponding file 
index = 5


# how to access hist data 



# how to access timing data: 



# how to access input deck parameters: 



# example: here's how to get the absolute times corresponding 
# to given data

