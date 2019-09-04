import sys 




# data container for the params. example usage: 
# x = AttrDict()
# x.a = 2
# x['a'] --> returns 2
# x.a --> returns 2 
# see https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute

class AttrDict( dict ):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def clear( self ) :
        for key in self.keys() :
            del self[ key ] 



class RecursiveAttrDict( AttrDict ) : 
    '''
        this is a subclass of the attrdict which gives support for recursive attrdict operations  
    '''
                
    def __str__( self, depth, accumulated_str, print_vals = False ) : 
        return self.attrdict2str( self, 0, '', print_vals )


    def prune( self, print_status = False ) : 
        recursively_prune_attrdict( self, None, None, print_status )

     
def attrdict2str( attrdict, depth, accumulated_str, print_vals ) : 


    #accumulated_str = ''

    # print( attrdict.keys() )

    try : 
        keys = sorted( attrdict.keys() )
        print( keys ) 
    except : 
        return ''

    for key in sorted( attrdict.keys() ):
        
        val = attrdict[ key ]

        if isinstance( val, AttrDict ) : 
            # print( k )
            currline = '---- ' * depth + '%s\n' % key
            
            
    #               currline += '\n'

            accumulated_str += currline + attrdict2str( val, depth + 1, accumulated_str )

        else : 
            if print_vals :
                accumulated_str += str( val )

    return accumulated_str




     

def recursively_prune_attrdict( current_attrdict, current_key, 
                                parent_attrdict, print_status = False ) : 
    '''
        iteratively remove all empty attr dicts
    '''

    # use a list here because .items() and .keys() return generators 
    # this avoids RuntimeError: dictionary changed size during iteration

    for key in list( current_attrdict.keys() ) : 
        val = current_attrdict[ key ]
        if isinstance( val, AttrDict ) : 
            recursively_prune_attrdict( val, key, current_attrdict, print_status )
    
    # perform the prune
    if parent_attrdict is not None and len( current_attrdict ) == 0 :

        if print_status : 
            print( 'Pruning key: %s' % current_key )
        del parent_attrdict[ current_key ] 

