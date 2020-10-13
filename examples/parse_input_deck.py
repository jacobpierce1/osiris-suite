# this example reads an input deck, changes the output, then 
# writes the modified input deck 
# the ability to load  the input deck in memory like this 
# makes data analysis and parameter scans much easier.

from osiris_suite import InputDeckManager 

input_deck_path = './test-data/test-data-2d/input.os' 

input_deck = InputDeckManager( input_deck_path ) 

# print in the fortran namelist format 
print( input_deck ) 

print( '\n\n')

# grab data for the first (0-indexed) zpulse 
zpulse_metadata = input_deck.get_metadata( 'zpulse', 0 )

# note that it's an OrderedDict. this data type is used 
# so that subsequent writes of the data are in the same order
# as the original.
print( 'zpulse_metadata: ')
print( zpulse_metadata )

print( '\n\n')


# get particular data 
a0 = zpulse_metadata[ 'a0' ]
print( 'a0 = %.2f' % a0 )


# modify deck and write it somewhere else 
zpulse_metadata[ 'a0' ] = 3
input_deck.write( './examples-output/input_modified.os' )


