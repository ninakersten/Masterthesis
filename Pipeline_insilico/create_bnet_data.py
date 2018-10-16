#This script creates .bnet files from 4 nodes, until 40 nodes #written by Nina Kersten 2018

import sys
import random
import string
import time
from time import*
import argparse
import os.path
#import os
#import errno

parser = argparse.ArgumentParser()
parser.add_argument('integers',type=int)
args = parser.parse_args()

#get the date and time
lt = localtime ()
jahr, monat, tag, hour, minute = lt [0:5]

#create list of letters
lowercase = list(string.ascii_lowercase)
uppercase = list(string.ascii_uppercase)
full_alpha_list = lowercase + uppercase
logic_list =[' & ']
#logic_list =[' & ',' | ']
sign_list =['!','']
secure_random = random.SystemRandom()


#amount of nodes for a network as default: (range(1,41))
for i in range(4,(args.integers)):
	alpha_list = full_alpha_list[:i]

	save_path = './PyBoolNet/bnet_data_insilico/'
	completeName = os.path.join(save_path, 'Network_'+ str(i) +'_' +str(tag) +'_'+ str(monat) +'_'+ str(jahr) +'_'+ str(hour) +'_'+ str(minute) + '.bnet')  
	write_bnet_file = open(completeName,"w") 

	#random_rule = [secure_random.choice(alpha_list), secure_random.choice(logic_list)]
	#print(random.choice(random_rule)())
	#for j in alpha_list:
		#random_rule = [x for x in range(1:4) ]
		#write_bnet_file.write(str(j) + ', ' + secure_random.choice(alpha_list) + secure_random.choice(logic_list) + secure_random.choice(alpha_list) + '\n')
		
		##first try:
		#random_rule = secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule2 =  secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule3 =  random_rule2 + secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule4 =  random_rule3 + secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule5 =  random_rule4 + secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule6 =  random_rule5 + secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule7 =  random_rule6 + secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule8 =  random_rule7 + secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule9 =  random_rule8 + secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)
		#random_rule10 =  random_rule9 + secure_random.choice(logic_list) + secure_random.choice(sign_list) + secure_random.choice(alpha_list)

		#second try:
		#random_rule = secure_random.choice(alpha_list)
		#list1=list(secure_random.choice(alpha_list))
		#list2=list(secure_random.choice(alpha_list))
		#for x in list1:
		#	for y in list2:
		#		if x != y:
		#			random_rule2 = '!' + x + ' & ' + y
		#			print(random_rule2)
		#		elif x == y:
		#			continue

		

		#random_rule2 = ' !' + secure_random.choice(alpha_list) + ' & ' + secure_random.choice(alpha_list)
		#print(random_rule2)
		#random_rule3 = ' !' + secure_random.choice(alpha_list) + ' & ' + secure_random.choice(alpha_list)
		#random_rule4 = secure_random.choice(alpha_list) + ' & ' + secure_random.choice(alpha_list)

		#third try:
		#random_rule =secure_random.choice(alpha_list)
		#random_rule_list1=list(secure_random.choice(alpha_list))
		#random_rule_list2=list(secure_random.choice(alpha_list))
		#print(random_rule_list2)
		#random_rule2 = ' !' + random_rule_list1 + ' & ' + [x for x in random_rule_list1 if x not in random_rule_list1]


		#random_rule3 = ' !' + secure_random.choice(alpha_list) + ' & ' + secure_random.choice(alpha_list)
		#random_rule4 = secure_random.choice(alpha_list) + ' & ' + secure_random.choice(alpha_list)

		#last try:
	random_rule = secure_random.choice(alpha_list)

	x=secure_random.choice(alpha_list)
		#print(x)
		#print(alpha_list)
	alpha_list.remove(x)
	y=secure_random.choice(alpha_list)

	random_rule2='!'+ x +' & ' + y
		#print(random_rule2)
	alpha_list.append(x)


	k=secure_random.choice(alpha_list)
		#print(k)
		#print(alpha_list)
	alpha_list.remove(k)
	i=secure_random.choice(alpha_list)

	random_rule3='!'+ k +' & ' + i
		#print(random_rule3)
	alpha_list.append(k)


	m=secure_random.choice(alpha_list)
		#print(m)
		#print(alpha_list)
	alpha_list.remove(m)
	n=secure_random.choice(alpha_list)

	random_rule4= m +' & ' + n
		#print(random_rule4)
	alpha_list.append(m)




	random_rule_list = [random_rule, random_rule2, random_rule3, random_rule4]
		
		#Problem: ODEfy macht Probleme bei doppelten Einträgen in der BooleanRule
		#write_bnet_file.write(str(j) + ', ' + random_rule + random.choice(random_rule_list) +'\n')
	for j in alpha_list:
		write_bnet_file.write(str(j) + ', ' + random.choice(random_rule_list) +'\n')



	write_bnet_file.close()
		



