from osiris_suite import AttrDict 

x = AttrDict( )
# x = dict( )

x[ 'a' ] = 2
print( x.a ) 

x.b = 3
print( x['b'] )