# example of what a script for parameter scans might look like,
# in this case for a parameter scan run on hoffman. 
# note that there may be system-specific ways by which batch scripts 
# are to be submitted. for example, on hoffman you are actually supposed
# to submit batch scripts using one submission script in batch mode.
# i've implemented 
# 

from osiris_suite import InputDeckManager 
import os 

batch_script = \
'''

'''

sim_path = './test-data/test-data-2d/'

# load input deck to be modfied 
input_deck_path = sim_path + 'input.os' 
deck = InputDeckManager( input_deck_path )


# this is the batch script we will keep using 
# one could also load this to memory and modify it just as 
# we are doing with the input deck. 
# this batch script just runs osiris, but you can also add something
# like "ipython analysis.py" to automatically run analysis at the end.
batch_script_path = sim_path + 'submit.sh'

# based on the way i've written this, we'll actually need the abs path.
batch_script_path = os.path.abspath( batch_script_path )

print( 'input_deck_path: ' + input_deck_path )
print( 'batch_script_path: ' + batch_script_path )
print( '\n' ) 

# with open( batch_script_path, 'r' ) as f : 
# 	batch_script = f.read()


scan_dir = './examples-output/parameter-scan-example/'
os.makedirs( scan_dir, exist_ok = True )

# parameter scan name conventions are beyond the scope of this lib, 
# so it's the user's responsibility to handle this construct 

a0_vals = [ 1, 2, 3 ] 

# grab data for the first (0-indexed) zpulse 
zpulse_metadata = deck.get_metadata( 'zpulse', 0 )

# get current directory for reference later 
owd = os.getcwd()

for a0 in a0_vals : 

	sim_path = scan_dir + 'a0=%d/' % a0 
	new_deck_path = sim_path + 'input.os' 

	os.makedirs( sim_path, exist_ok = True )

	zpulse_metadata[ 'a0' ] = a0 

	deck.write( new_deck_path )

	print( 'wrote new input deck: ' + new_deck_path )

	# run the script. see note at beginning.
	command = 'qsub %s' % batch_script_path
	
	print( 'cd ' + sim_path )
	print( command )

	os.chdir( sim_path )
	os.system( command )

	# go back to original directory 
	print( 'cd ../' )
	os.chdir( owd )


	