#Scoring program for calculating Accuracy, Precision and Recall, written by Nina Kersten#
#This program runs an example for real data

import sys,os, re
import csv
import itertools
import ast
import math


#Read in the names_lists for the cartesian product
names_list1 = ["a","b","c","d"];
names_list2 = ["a","b","c","d"];


#Create the cartesian productof the names
names_list = []
for i in itertools.product(names_list1,names_list2):
	names_list.append(i)


#Converting the "\t"-seperated Goldstandard network into a whitespace seperated network
with open("./SIF_files/network4_goldstandard.sif","r") as fin, open ("./SIF_files/goldstandard1.sif","w") as fout:
	for line in fin:
		fout.write(line.replace('\t',' '))

#Read in the Golstandard and the Prediction data set
gold_file = open("./SIF_files/goldstandard1.sif","r")
pred_file = open("./SIF_files/network4_200_b3_sol_main.sif","r")
print("b3_sol=200")

line1 = gold_file.readlines()
line2 = pred_file.readlines()
#print(line1,line2)

line1 = [elem.replace('\n','').replace(' 1, -1 ',' 1 ').replace(' -1 ',' 1 ') for elem in line1]
line2 = [elem.replace('\n','').replace(' 1, -1 ',' 1 ').replace(' -1 ',' 1 ') for elem in line2]
#print(line1,line2)

line1 = [e for e in line1 if e not in ('')]
line2 = [e for e in line2 if e not in ('')]
#print(line1, line2)

#Calculating True Positive
tp_biglist = []
fn_biglist = []
for gold in line1:
	if gold in line2:
		tp_list = list(gold)
		#print(tp_biglist)
		tp_list = ''.join(gold)
		#print(tp_biglist)
		tp_list = tp_list.strip().split()
		tp_list = [e for e in tp_list if e not in ('1')]
		tp_biglist.append(tuple(tp_list))
		#print(tp_biglist)
		tp = len(tp_biglist)
		#print(tp_biglist) #[('a1a', 'b2b'), ('a1a', 'c3c'), ('e5e', 'a1a')]

#Calculating False Negative
	elif gold not in line2:
		fn_list = list(gold)
		fn_list = ''.join(gold)
		fn_list = fn_list.strip().split()
		fn_list = [e for e in fn_list if e not in ('1')]
		fn_biglist.append(tuple(fn_list))
		#fn_biglist = [t for t in fn_biglist if t != ()]
		fn = len(fn_biglist)

#print(tp_biglist)		

#Calculating False Positive
fp_biglist = []
for pred in line2:
	if pred not in line1:
		fp_list = list(pred)
		fp_list = ''.join(pred)
		fp_list = fp_list.strip().split()
		fp_list = [e for e in fp_list if e not in ('1')]
		fp_biglist.append(tuple(fp_list))
		#fp_biglist = [t for t in fp_biglist if t != ()]
		fp = len(fp_biglist)


#Deleting TP, FN, FP from the names_list2 to get finally the TN-value
def EmptyList1(tp_biglist):
	if len(tp_biglist) == 0:
		return 0
	else:
		return 1
           
if EmptyList1(tp_biglist): 
	for tp_string in tp_biglist:
		if tp_string in names_list:
			names_list.remove(tp_string)
else:
	tp = 0


#print(len(names_list))

def EmpytList2(fp_biglist):
	if len(fp_biglist) == 0:
		return 0
	else:
		return 1

if EmpytList2(fp_biglist): 
	for fp_string in fp_biglist:
		if fp_string in names_list:
			names_list.remove(fp_string)
else:
	fp = 0

#print(len(names_list))

def EmpytList3(fn_biglist):
	if len(fn_biglist) == 0:
		return 0
	else:
		return 1

if EmpytList3(fn_biglist): 
	for fn_string in fn_biglist:
		if fn_string in names_list:
			names_list.remove(fn_string)
else:
	fn = 0

#print(len(names_list))
		

tn = len(names_list)

print("True Positive Value =",tp)
print("True Negative Value =",tn)
print("False Positive Value =",fp)
print("False Negative Value =",fn)


#Berechnung von Accuracy, Prcision und Recall
acc = ((tp+tn)/(tp+tn+fp+fn))
print("Accuracy =",acc)
pre = ((tp)/(tp+fp))
print("Precision =",pre)
rec = ((tp)/(tp+fn))
print("Recall =",rec)

#Calculating Matthiews correlation coefficient(MCC):
mcc = ((tp*tn-fp*fn)/(math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))))
print("Matthiews correlation coefficient (MCC) = ",mcc)

#Balanced  Accuracy
bacc = (((tp/(tp+fn))+(tn/(fp+tn)))/2)
print("Balanced Accuracy =",bacc)

