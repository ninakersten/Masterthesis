##Scoring program for calculating Precision, Recall and Accuracy of a Goldstandard network against it's Prediction####writte by Nina Kersten 2018
import sys,os, re
import csv
import itertools


#Importing a .csv file for a certain cellline, getting the names of the proteins
rows = csv.reader(open("./example/BT20_main.csv", "r"), delimiter=',')
arows = [row for row in rows if "Antibody Name" in row]
arows1= arows[0]
arows2 = [x for x in arows1 if x]
arows2.remove("Antibody Name")

names_list1 = arows2 
names_list2 = arows2

#Creating a list of tuples of all possible combinations of the names
names_list = []
for i in itertools.product(names_list1,names_list2):
	#print(i)
	names_list.append(i)
#print(len(names_list))

#Converting the "\t"-seperated Goldstandard network into a whitespace seperated network
with open("./realdata_example/Goldstandard.sif","r") as fin, open ("./realdata_example/Goldstandard1.sif","w") as fout:
	for line in fin:
		fout.write(line.replace('\t',' '))
#print(fout)



#Read in the Golstandard and the Prediction data set
gold_file = open("./realdata_example/Goldstandard1.sif","r")
pred_file = open("./realdata_example/Prediction.sif","r")



line1 = gold_file.readlines()
line2 = pred_file.readlines()
#print(line1)

line1 = [elem.replace('\n','').replace('1, -1','1').replace('-1','1') for elem in line1]
line2 = [elem.replace('\n','').replace('1, -1','1').replace('-1','1') for elem in line2]
#print(line2)

#Calculating True Positive
tp_biglist = []
for gold in line1:
	if gold in line2:
		tp_list = list(gold)
		tp_list = ''.join(gold)
		#print(tp_list)
		tp_list = tp_list.strip().split()
		tp_list = [e for e in tp_list if e not in (' ', '1')]
		tp_biglist.append(tuple(tp_list))
		tp_biglist = [t for t in tp_biglist if t != ()]
		tp = len(tp_biglist)
	else:
		tp = 0

#print(tp)


#Calculating False Negative
fn_biglist = []
for gold in line1:
	if gold not in line2:
		fn_list = list(gold)
		fn_list = ''.join(gold)
		fn_list = fn_list.strip().split()
		fn_list = [e for e in fn_list if e not in (' ', '1')]
		fn_biglist.append(tuple(fn_list))
		fn = len(fn_biglist)
	#else:
	#	tn = 0
#print(fn_biglist)


#Calculating False Positive
fp_biglist = []
for pred in line2:
	if pred not in line1:
		fp_list = list(pred)
		fp_list = ''.join(pred)
		fp_list = fp_list.strip().split()
		fp_list = [e for e in fp_list if e not in (' ', '1')]
		fp_biglist.append(tuple(fp_list))
		fp_biglist = [t for t in fp_biglist if t != ()]
		fp = len(fp_biglist)
	#else:
	#	fp = 0


#Calculating the True Negative value by deleting the name pairs from the list of name combinations created above
for tp_string in tp_biglist:
	if tp_string in names_list:
		names_list.remove(tp_string)
	elif not tp_biglist:
		break



for fp_string in fp_biglist:
	if fp_string in names_list:
		names_list.remove(fp_string)
	#elif not fp_biglist:
	#	break


for fn_string in fn_biglist:
	if fn_string in names_list:
		names_list.remove(fn_string)
	#elif not fn_biglist:
	#	break


		tn = len(names_list)

print("True Negative Value =",tn)
print("False Positive Value =",fp)
print("True Positive Value =",tp)
print("False Negative Value =",fn)


#Calculating the Accuracy, Recall and Precision
acc = ((tp+tn)/(tp+tn+fp+fn))
print("Accuracy =",acc)
pre = ((tp)/(tp+fp))
print("Precision =",pre)
rec = ((tp)/(tp+fn))
print("Recall =",rec)
