# this example reads an input deck, changes the output, then 
# writes the modified input deck 


from osiris_suite import InputDeckManager 

input_deck = './input.os' 

deck = InputDeckManager( input_deck ) 

print( deck ) 



deck.write( './input_modified.os' )


