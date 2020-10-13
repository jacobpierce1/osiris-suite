from osiris_suite import OsirisDataContainer
import matplotlib.pyplot as plt 
import numpy as np
import colorcet 


data_path = './test-data/test-data-2d/'
input_deck_path = data_path + 'input.os'

# input deck path is not necessary to specify, but for 
# most applications having the input deck data in memory will
# be useful. 
osdata = OsirisDataContainer( data_path, input_deck_path = input_deck_path )

# hist data isn't loaded by default because you might not want it. 
# same with timings. load em here. 
osdata.load_hist()
osdata.load_timings() 


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
index = 10

data, axes = e1.file_managers[ index ].unpack() 

fig, axarr = plt.subplots( 1, 2 ) 
ax = axarr[0]
ax.imshow( data, cmap = colorcet.m_CET_D3 ) 
ax.set_title( 'E1 (Easy money!)' )

# how to access hist data 
electron_ke_data = osdata.data.hist.par01_ene[  'KinEnergy' ]
electron_ke_times = osdata.data.hist.par01_ene[ 'Time' ]
ax = axarr[1]
ax.plot( electron_ke_times, electron_ke_data )
ax.set_title( 'Electron KE vs. Time \n(Full send!)')


# how to access timing data: 
# timing data not supported yet, but the below line of code will run
# eventually 
# print( osdata.data.timings )


# how to access input deck parameters (see parse_input_deck for more)
# examples: 
zpulse_metadata = osdata.input_deck.get_metadata( 'zpulse', 0 )
a0 = zpulse_metadata[ 'a0']
print( 'a0 = %.2f' % a0 )


# another input deck example: here's how to get the absolute times 
# corresponding to the above electric field data
timestep_metadata = osdata.input_deck.get_metadata( 'time_step')
dt = timestep_metadata[ 'dt' ]
ndump = timestep_metadata[ 'ndump' ]

abs_times = np.array( timesteps ) * dt * ndump

print( 'abs_times: ' + str( abs_times ) )

plt.show() 
