import sys,os, re
import csv
import itertools
import collections
import ast

from collections import OrderedDict
from itertools import chain


#Read in the names_lists for the cartesian product
names_list1 = ["A","B","C","D","E"];
names_list2 = ["A","B","C","D","E"];

#Getting the names_list from the csv_file
#with open("./example/BT20_main.csv","r") as csvfile:
		#reader = csv.reader(csvfile, delimiter = ',')
		#names_list = []
		#for row in reader:
			#print(row[1])
			#names_list = (row[1])
			# take list from row containing the Antibodies Name
			#names_list.append(names_list)

					#print(names_list)
#alternative:
		#my_list = list(reader)
		#names_list = my_list[0]
		#print(names_list)


#Read in the Golstandard and the Prediction data set
gold_file = open("./example/goldstandard.sif","r")
pred_file = open("./example/prediction.sif","r")

#Create the cartesian productof the names
names_list = []
for i in itertools.product(names_list1,names_list2):
	#print(i)
	names_list.append(i)
	#names_list2 = []
	#for z in names_list:
	#	names_list2.append((''.join([w+' ' for w in z])).strip())
	#names_list2 = [x.replace(' ','') for x in names_list]

print(names_list)

line1 = gold_file.readlines()
line2 = pred_file.readlines()


#Calculating True Positive
tp_biglist = []
for gold in line1:
	if gold in line2:
		tp_list = list(gold)
		tp_list = [e for e in tp_list if e not in (' ', '1','\n')]
		tp_biglist.append(tuple(tp_list))
		tp_biglist = [t for t in tp_biglist if t != ()]
		tp = len(tp_biglist)


#Calculating False Negative
fn_biglist = []
for gold in line1:
	if gold not in line2:
		fn_list = list(gold)
		fn_list = [e for e in fn_list if e not in (' ', '1','\n')]
		fn_biglist.append(tuple(fn_list))
		fn_biglist = [t for t in fn_biglist if t != ()]
		fn = len(fn_biglist)

		

#Calculating False Positive
fp_biglist = []
for pred in line2:
	if pred not in line1:
		fp_list = list(pred)
		fp_list = [e for e in fp_list if e not in (' ', '1','\n')]
		fp_biglist.append(tuple(fp_list))
		fp_biglist = [t for t in fp_biglist if t != ()]
		fp = len(fp_biglist)


#Deleting TP, FN, FP from the names_list2 to get finally the TN-value
for tp_string in tp_biglist:
		if tp_string in names_list:
			names_list.remove(tp_string)


for fp_string in fp_biglist:
	if fp_string in names_list:
		names_list.remove(fp_string)

for fn_string in fn_biglist:
	if fn_string in names_list:
		names_list.remove(fn_string)

		tn = len(names_list)


print("True Negative Value =",tn)
print("False Positive Value =",fp)
print("True Positive Value =",tp)
print("False Negative Value =",fn)


#Berechnung von Accuracy, Prcision und Recall
acc = ((tp+tn)/(tp+tn+fp+fn))
print("Accuracy =",acc)
pre = ((tp)/(tp+fp))
print("Precision =",pre)
rec = ((tp)/(tp+fn))
print("Recall =",rec)


