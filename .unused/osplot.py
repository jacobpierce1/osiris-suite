
import click 

import plotters



@click.group() 
def cli() : 
	pass 


@click.command( 'nci' ) 
@click.option( '--path', default='./' )
@click.option( '--timestep', default=0 )

def plot_nci( path, timestep ) : 	
	# click.echo( 'plotting nci' )
	# print( timestep )

	plotters.plot_nci( path, timestep ) 


@click.command( 'laser' ) 
@click.option( '--data_path', default = './' )
@click.option( '--savedir', default = None )
@click.option( '--n_frames', default = 10 )
@click.option( '--timesteps', default = None )

# @click.option( '--timestep', default=0 )

def plot_laser( data_path, savedir, n_frames, timesteps ) :

	plotters.plot_laser( data_path, savedir )


@click.command( 'plot-q3d' ) 
@click.option( '--data_path', default = './' )
@click.option( '--index', default = None )
@click.option( '--savedir', default = None )
@click.option( '--title', default = '' )
@click.option( '--nproc', default = 1 )
@click.option( '--stride', default = 1 )
@click.option( '--duration', default = 10 )

def plot_q3d( data_path, index, savedir, title, nproc, 
				stride, duration  ) : 

	plotters.plot_q3d( data_path, index, savedir, title, nproc, 
				stride, duration  )


@click.command( 'plot-all-leaves' ) 
@click.option( '--data_path', default = './' )
@click.option( '--index', default = None )
@click.option( '--savedir', default = None )
@click.option( '--title', default = '' )
@click.option( '--nproc', default = 1 )
@click.option( '--stride', default = 1 )
@click.option( '--duration', default = 10 )

def plot_all_leaves( data_path, index, savedir, title, nproc, 
				stride, duration  ) : 

	plotters.plot_all_leaves( data_path, index, savedir, title, nproc, 
								stride, duration  )





@click.command( ) 
def scratch( ) : 
	plotters.scratch() 




cli.add_command( plot_nci )
cli.add_command( plot_laser )
cli.add_command( plot_q3d ) 
cli.add_command( plot_all_leaves )

cli()