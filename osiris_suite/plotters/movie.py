from osiris_suite import OsirisDataContainer
import osiris_suite.utils as utils 
import colorcet 
from pprint import pprint 
import numpy as np 
import os 

import matplotlib
# matplotlib.use('TkAgg') # <-- THIS MAKES IT FAST!
import matplotlib.pyplot as plt 

cmaps = { 
		'div' : colorcet.m_CET_D1A,
		'lin' : colorcet.m_biy,
		'rainbow' : colorcet.m_rainbow
	}




def movie( ) : 

	# check if there are time conflicts 



