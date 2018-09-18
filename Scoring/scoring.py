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
	names_list2 = []
	for z in names_list:
		names_list2.append((''.join([w+' ' for w in z])).strip())
		names_list2 = [x.replace(' ','') for x in names_list2]
	
print(names_list2)



line1 = gold_file.readlines()
line2 = pred_file.readlines()

tup_list = []
for gold in line1:
	#print (gold)
	for pred in line2:
		#print(pred)
		#Calculating True Positive
		if pred == gold:
			#Speicher die tp-Fälle als Tupel
			tp_list = (pred,gold)
			#print(tp_list)

			tp_list1 = list(tp_list)

			tp_list2 = [x.replace('\n','').replace('1','').replace(',','') for x in tp_list1]

			tp_list4 = list(OrderedDict.fromkeys(tp_list2))

			tup_li = [x.replace(' ','') for x in tp_list4]

			tup_list.append(tup_li)



new_list = list(chain(*tup_list))
tp = len(new_list)



#Calculating False Negative
fn_biglist = []
for gold in line1:
	if gold not in line2:
		fn_list = list(gold)
		#print(fn_list)
		fn_list = [e for e in fn_list if e not in (' ', '1','\n')]
		fn_biglist.append(tuple(fn_list))
		fn = len(fn_biglist)

		

#Calculating False Positive
fp_biglist = []
for pred in line2:
	if pred not in line1:
		fp_list = list(pred)
	
		fp_list = [e for e in fp_list if e not in (' ', '1','\n')]
		#print(fp_list)
		fp_biglist.append(tuple(fp_list))
		
		fp_biglist = [t for t in fp_biglist if t != ()]

		fp = len(fp_biglist)




#Deleting TP, FN, FP from the names_list2 to get finally the TN-value
for string in new_list:
	if string in names_list2:
		names_list2.remove(string)
		tn = len(names_list2)


print("False Positive Value =",fp)
print("True Positive Value =",tp)
print("False Negative Value =",fn)
print("True Negative Value =",tn)

#Berechnung von Accuracy, Prcision und Recall
acc = ((tp+tn)/(tp+tn+fp+fn))
print("Accuracy =",acc)
pre = ((tp)/(tp+fp))
print("Precision =",pre)
rec = ((tp)/(tp+fn))
print("Recall =",rec)


