
import sys,os, re
import csv
import itertools
import ast
import math

#s = os.listdir('./goldstandard_insilico')
#print(s)
##########################################################
#for file_name in os.listdir('./goldstandard_insilico'):
#	if file_name in os.listdir('./prediction_insilico'):
#		file_1_path = os.path.join('./goldstandard_insilico', file_name)
#		#print(file_1_path)
#		file_2_path = os.path.join('./prediction_insilico', file_name)
#		print(file_2_path)
##############################################################	
	#f1=open(file_1_path,'r')
	#f2=open(file_2_path,'r')
	#if f1 == f2:
	#	print("They are equal!")
		
	#elif f1 != f2:
		#print("FALSE!!!")

import filecmp
import os

# Determine the items that exist in both directories
d1_contents = set(os.listdir('./goldstandard_insilico'))
d2_contents = set(os.listdir('./prediction_insilico'))
common = list(d1_contents & d2_contents)
print(common)
for f in common:
	args1= str(os.path.join('./goldstandard_insilico', f))
	print(args1)
	args2= os.path.join('./prediction_insilico', f)
	print(args2)



#common_files = [ f for f in common if os.path.isfile(os.path.join('./goldstandard_insilico', f))]
#print('Common files:', common_files)



# Compare the directories
#match, mismatch, errors = filecmp.cmpfiles('./goldstandard_insilico', 
#                                           './prediction_insilico', 
 #                                          common_files)
#print(match)
#print 'Mismatch:', mismatch
#print 'Errors:', errors