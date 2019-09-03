import sys 


class RecursiveAttrDict( dict ) : 

    # pythonic style: give user the option of creating a recursive dict if they
    # already had the appropriate data structure stored.
    # also allows you to create an object with no keys. compare to empty,
    # which does the same thing but also allows you to populate with a list of key names
    def __init__( self, data = None, size = 0 ) :

        if data is None :
            data = {} 

        self.data = data 

        # if data is already available (i.e. its not empty) then set current length
        # to be size of the first array 
        if self.data : 
            self.size = len( next( iter( data.values() ) ) )

        else : 
            self.size = size

        # if data was passed in, we need to make sure that the data is in a
        # valid state (all array lengths are the same).
        self.check_good() 


    # here is how it works: if item is one of the keys, then call it as if you
    # requested series[ item ]
    # otherwise just give the normal attribute
    # this way you don't lose access to normal attributes such as len, keys, __dict__, etc.
    def __getattr__( self, item ) :
        if item in self.data.keys() :
            return self[ item ]
        elif item in self.__dict__ :
            return self.item
        else :
            raise AttributeError( 'ERROR: the following is not an attribute: %s' % item ) 

            
    def __getitem__( self, item ) :

        # if string, then return the dict evaluated at the key 
        if isinstance( item, str ) :
            return self.data[ item ]  
            
        # otherwise assume it's an int and apply the index
        else :
            return AttrDict( { key : val[ item ] for key, val in self.data.items() } )

            
    # check if all the arrays have the same length and all the keys are strings
    # terminate program if not .       
    def check_good( self ) :
        for key in self.data.keys() :
            if not isinstance( key, str ) :
                # return 0
                print( 'ERROR: all data keys for RecursiveDict must be strings' )
                sys.exit(1)
                
            if len( self.data[ key ] ) != self.size :
                print( 'ERROR: arrays don\'t all have same len' )
                sys.exit( 1 )  


    # set a key equal to data. the key used can also be a new key not
    # already in self.data
    def __setitem__( self, key, data ) :
        if not hasattr( data, '__len__' ) :
            data = [ data for i in range( self.size ) ] 
        self.data[ key ] = data

        
    # create an empty RecursiveDict
    @classmethod
    def empty( cls, keys = None, size = 0 ) :         
        if keys is None :
            keys = [] 

        data = {} 
        
        for key in keys :
            data[ key ] = [ None for i in range(size) ] 

        return cls( data, size = size ) 
            
            
    def keys( self ) :
        return self.data.keys()

    def __len__( self ) :
        return self.size 
        
    def __str__( self ) :
        return str( self.data ) 
        
    def __repr__( self ) :
        return str( self ) 

    def clear( self ) :
        # for key in self.data.keys() :
        #     del self.data[ key ]
        self.data.clear() 
        self.size = 0 

    # resize all the arrays 
    def set_size( self, size ) :
        # print( 'new size: ' + str( size ) ) 

        if size == self.size :
            return 

        # if new size is larger, then extend with empty data 
        elif size > self.size : 
            for key in self.data.keys() : 
                self.data[ key ].extend( [ None for i in range( size - self.size ) ] )

        # if new size is smaller then keep deleting the rear elements until size matches.
        else :
            for key in self.data.keys() :
                for i in range( self.size - size ) : 
                    del self.data[ key ][-1] 
                
        self.size = size     
        
        




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





