#Scoring program for calculating Accuracy, Precision and Recall, written by Nina Kersten#
#This program runs an example for real data


import sys,os, re
import csv
import itertools
import ast
import math
import filecmp
import numpy as np
import argparse
import shlex

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Wrong input.")
		sys.exit()
	bin_method = sys.argv[1]
	learn_method = sys.argv[2]
	#print(len(sys.argv))

	#write result to .csv file
	with open('scoring_result.csv', mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter =',')
		csv_writer.writerow(['Networkname','Nodes','Bin_method','Learn_method','Timepoints','Runtime_in_sec.','TP','TN','FP','FN','Pre','Rec','ACC','BACC','MCC'])
		#csv_writer.writerow(['Networkname','Timepoints','binmethod','learnmethod','TP','TN','FP','FN','Pre','Rec','ACC','BACC','MCC'])

		d1_contents = set(os.listdir('./goldstandard_realdata'))
		d2_contents = set(os.listdir('./prediction_realdata'))
		common = list(d1_contents & d2_contents)

		mean_bacc_list=[]
		mean_mcc_list=[]
		mean_nodes_list=[]
		mean_timepoints_list=[]
		mean_acc_list=[]
		mean_pre_list=[]
		mean_rec_list=[]
		mean_runtime_list=[]


		#print(common)
		for f in common:
			args1= os.path.join('./goldstandard_realdata', f)
			args2= os.path.join('./prediction_realdata', f)
			#print(f)
			args3= f.replace('Serum.sif','.csv').replace('Insulin.sif','.csv').replace('PBS.sif','.csv').replace('IGF1.sif','.csv').replace('HGF.sif','.csv').replace('EGF.sif','.csv').replace('FGF1.sif','.csv').replace('NRG1.sif','.csv')
			#print(args3)
			args6=f.replace('.sif','.txt').replace('.sif','.txt').replace('.sif','.txt').replace('.sif','.txt').replace('.sif','.txt').replace('.sif','.txt').replace('.sif','.txt').replace('.sif','.txt')
			args4= os.path.join('./CSV_realdata',args3)
			args5= os.path.join('./CSV_realdata_2_TXT',args6)
			#print(args4)

			#Importing a .csv file for a certain cellline, getting the names of the proteins
			rows = csv.reader(open(args4, "r"), delimiter=',')
			timepoints = sum(1 for line in open(args5))-2
			mean_timepoints_list.append(timepoints)
			arows = [row for row in rows if "Antibody Name" in row]
			arows1= arows[0]
			#print(arows1)
			arows2 = [x for x in arows1 if x]
			arows2.remove("Antibody Name")
			nodes=len(arows2)
			mean_nodes_list.append(nodes)
			
			#print(arows2)

			names_list1 = arows2
			names_list2 = arows2

			#names_list1 = ["a","b","c","d"];
			#names_list2 = ["a","b","c","d"];

			#Create the cartesian productof the names
			names_list = []
			for i in itertools.product(names_list1,names_list2):
				names_list.append(i)


			#Converting the "\t"-seperated Goldstandard network into a whitespace seperated network
			#with open(args1,"r") as fin, open (args1,"w") as fout:
			#	for line in fin:
			#		fout.write(line.replace('\t',' '))
			#print(fout)

						#write runtime into the scoring.csv
			runtime_file = open('runtime.txt','r')
			runtime1 = runtime_file.readlines()
			runtime_name_compare=f.replace('.sif','')
			#print(runtime_name_compare)
			runtime2 = [time.replace('./CSV_realdata_2_TXT/','').replace('.txt','').replace('\n','') for time in runtime1]
			#shlex.split(runtime2)
			for run in runtime2:
				run1=shlex.split(run)
				#print(run1)
				if run1[0]==runtime_name_compare:
					run2=int(run1[1])
					#print(run2)
					mean_runtime_list.append(run2)

			#Read in the Golstandard and the Prediction data set
			gold_file = open(args1,"r")
			pred_file = open(args2,"r")


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

			#print("True Positive Value =",tp)
			#print("True Negative Value =",tn)
			#print("False Positive Value =",fp)
			#print("False Negative Value =",fn)


			#Berechnung von Accuracy, Prcision und Recall
			
			if tp+fp==0:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				bacc = (acc/2)
				rec = ((tp)/(tp+fn))
				pre = 'No Value'
				mcc = 'No Value'
				mean_bacc_list.append(bacc)
				mean_rec_list.append(rec)
				mean_acc_list.append(acc)
			elif tp+fn==0:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				bacc = (acc/2)
				pre = ((tp)/(tp+fp))
				mcc = 'No Value'
				rec = 'No Value'
				mean_bacc_list.append(bacc)
				mean_rec_list.append(rec)
				mean_pre_list.append(pre)
			elif tn+fp==0:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				bacc = (acc/2)
				pre = ((tp)/(tp+fp))
				rec = ((tp)/(tp+fn))
				mcc = 'No Value'
				mean_bacc_list.append(bacc)
				mean_acc_list.append(acc)
				mean_rec_list.append(rec)
				mean_pre_list.append(pre)
			elif tn+fn==0:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				bacc = (acc/2)
				pre = ((tp)/(tp+fp))
				rec = ((tp)/(tp+fn))
				mcc = 'No Value'
				mean_bacc_list.append(bacc)
				mean_acc_list.append(acc)
				mean_rec_list.append(rec)
				mean_pre_list.append(pre)
			elif tp+tn+fp+fn==0:
				acc = 'No Value'
				bacc = 'No Value'
				pre = 'No Value'
				rec = 'No Value'
				mcc = 'No Value'
			#elif tp!=0 and tn!=0 and fp!=0 and fn!=0:
			else:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				pre = ((tp)/(tp+fp))
				rec = ((tp)/(tp+fn))
				mcc = ((tp*tn-fp*fn)/(math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))))
				bacc = (acc/2)
				mean_bacc_list.append(bacc)
				mean_mcc_list.append(mcc)
				mean_acc_list.append(acc)
				mean_rec_list.append(rec)
				mean_pre_list.append(pre)

			csv_writer.writerow([f,str(nodes),str(bin_method),str(learn_method),str(timepoints),str(run2),str(tp),str(tn),str(fp),str(fn),str(pre),str(rec),str(acc),str(bacc),str(mcc)])
	
		if mean_bacc_list!=[] and mean_mcc_list!=[]:	
			mean_bacc=(sum(mean_bacc_list)/len(mean_bacc_list))
			mean_mcc=(sum(mean_mcc_list)/len(mean_mcc_list))
		elif mean_bacc_list!=[] and mean_mcc_list==[]:
			mean_bacc=(sum(mean_bacc_list)/len(mean_bacc_list))
			mean_mcc='No Value'
		elif mean_bacc_list==[] and mean_mcc_list!=[]:
			mean_mcc=(sum(mean_mcc_list)/len(mean_mcc_list))
			mean_bacc='No Value'

		if mean_acc_list==[]:
			mean_acc='No Value'
		elif mean_acc_list !=[]:
			mean_acc=(sum(mean_acc_list)/len(mean_acc_list))

		if mean_rec_list==[]:
			mean_rec='No Value'
		elif mean_rec_list !=[]:
			mean_rec=(sum(mean_rec_list)/len(mean_rec_list))

		if mean_pre_list==[]:
			mean_pre='No Value'
		elif mean_pre_list !=[]:
			mean_pre=(sum(mean_pre_list)/len(mean_pre_list))

		if mean_nodes_list==[]:
			mean_nodes='No Value'
		elif mean_nodes_list !=[]:
			mean_nodes=(sum(mean_nodes_list)/len(mean_nodes_list))

		if mean_timepoints_list==[]:
			mean_timepoints='No Value'
		elif mean_timepoints_list !=[]:
			mean_timepoints=(sum(mean_timepoints_list)/len(mean_timepoints_list))

		#print(mean_runtime_list)
		if mean_runtime_list==[]:
			mean_runtime='No Value'
		elif mean_runtime_list !=[]:
			mean_runtime=(sum(mean_runtime_list)/len(mean_runtime_list))
			
		#print(mean_mcc)
		#print(mean_bacc)
		csv_writer.writerow([''])
		csv_writer.writerow(['Mean_Nodes',str(mean_nodes)])
		csv_writer.writerow(['Mean_Timepoints',str(mean_timepoints)])
		csv_writer.writerow(['Mean_Runtime',str(mean_runtime)])
		csv_writer.writerow(['Mean_BACC',str(mean_bacc)])
		csv_writer.writerow(['Mean_MCC',str(mean_mcc)])
		csv_writer.writerow(['Mean_ACC',str(mean_acc)])
		csv_writer.writerow(['Mean_Precision',str(mean_pre)])
		csv_writer.writerow(['Mean_Recall',str(mean_rec)])




	csv_file.close()