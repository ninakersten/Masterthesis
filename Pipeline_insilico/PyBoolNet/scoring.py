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

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong input.")
        sys.exit()
    name_of_bnet_file1 = sys.argv[1]
    name_of_bnet_file = sys.argv[2]
    print(len(sys.argv))
    print(name_of_bnet_file1)

    """
	parser = argparse.ArgumentParser()
	parser.add_argument("dir", help="Enter the directory of the ./TS2B_output/output2.bnet -file")
	args = parser.parse_args()
	print(args[1])

	#print(args)
	#args, unknown = parser.parse_known_args()


	#Read in the names_lists for the cartesian product
	#names_list1 = ["4EBP1_pS65","4EBP1_pT37_pT46","ACC_pS79","AKT_pS473","AKT_pT308"]
	#names_list2 = ["4EBP1_pS65","4EBP1_pT37_pT46","ACC_pS79","AKT_pS473","AKT_pT308"]

	#write result to .txt file
	#completeName = 'scoring.txt'
	#write_scoring_file = open(completeName, "w")

	#write result to .csv file
	with open('scoring_result.csv', mode='w') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter =',')
		csv_writer.writerow(['Networkname','Timepoints','TP','TN','FP','FN','Pre','Rec','ACC','BACC','MCC'])
		#csv_writer.writerow(['Networkname','Timepoints','binmethod','learnmethod','TP','TN','FP','FN','Pre','Rec','ACC','BACC','MCC'])

		d1_contents = set(os.listdir('./goldstandard_insilico'))
		d2_contents = set(os.listdir('./prediction_insilico'))
		common = list(d1_contents & d2_contents)
		#print(common)
		for f in common:
			args1= os.path.join('./goldstandard_insilico', f)
			args2= os.path.join('./prediction_insilico', f)
			#print(f)
			args3= f.replace('.sif','.csv')
			#print(args3)
			args4= os.path.join('./CSV_insilico',args3)
			#print(args4)

			#Importing a .csv file for a certain cellline, getting the names of the proteins
			rows = csv.reader(open(args4, "r"), delimiter=',')
			arows = [row for row in rows if "Antibody Name" in row]
			arows1= arows[0]
			#print(arows1)
			arows2 = [x for x in arows1 if x]
			arows2.remove("Antibody Name")
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
			#if (tp+tn+fp+fn)== 0;
		
		
			#acc = ((tp+tn)/(tp+tn+fp+fn))
			#print("Accuracy =",acc)
			#pre = ((tp)/(tp+fp))
			#print("Precision =",pre)
			#np.seterr(divide='ignore', invalid='ignore')
			#rec = ((tp)/(tp+fn))
			#print("Recall =",rec)

			#Calculating Matthiews correlation coefficient(MCC):
			#mcc = ((tp*tn-fp*fn)/(math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))))
			#print("Matthiews correlation coefficient (MCC) = ",mcc)

			#Balanced  Accuracy
			#bacc = (((tp/(tp+fn))+(tn/(fp+tn)))/2)
			#print("Balanced Accuracy =",bacc)


			#write_scoring_file.write("True Positive Value =" + str(tp) + '\n')
			#write_scoring_file.write("True Negative Value =" + str(tn) + '\n')
			#write_scoring_file.write("False Positive Value =" + str(fp) + '\n')
			#write_scoring_file.write("False Negative Value =" + str(fn) + '\n')
			#write_scoring_file.write("Accuracy =" + str(acc) +'\n')
			#write_scoring_file.write("Precision =" + str(pre) + '\n')
			#write_scoring_file.write("Recall =" + str(rec) + '\n')
			#write_scoring_file.write("Matthiews correlation coefficient (MCC) = " + str(mcc) + '\n')
			#write_scoring_file.write("Balanced Accuracy ="+ str(bacc))
			if tp+fp==0:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				bacc = (((tp/(tp+fn))+(tn/(fp+tn)))/2)
				rec = ((tp)/(tp+fn))
				pre = 'No Value'
				mcc = 'No Value'
			elif tp+fn==0:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				bacc = (((tp/(tp+fn))+(tn/(fp+tn)))/2)
				pre = ((tp)/(tp+fp))
				mcc = 'No Value'
				rec = 'No Value'
			elif tn+fp==0:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				bacc = (((tp/(tp+tn))+(tn/(fp+fn)))/2)
				pre = ((tp)/(tp+fp))
				rec = ((tp)/(tp+fn))
				mcc = 'No Value'
			elif tn+fn==0:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				bacc = (((tp/(tp+tn))+(tn/(fp+fn)))/2)
				pre = ((tp)/(tp+fp))
				rec = ((tp)/(tp+fn))
				mcc = 'No Value'
			elif tp+tn+fp+fn==0:
				acc = 'No Value'
				bacc = 'No Value'
				pre = 'No Value'
				rec = 'No Value'
				mcc = 'No Value'
			else:
				acc = ((tp+tn)/(tp+tn+fp+fn))
				#print("Accuracy =",acc)
				pre = ((tp)/(tp+fp))
				#print("Precision =",pre)
				#np.seterr(divide='ignore', invalid='ignore')
				rec = ((tp)/(tp+fn))
				#print("Recall =",rec)

				#Calculating Matthiews correlation coefficient(MCC):
				mcc = ((tp*tn-fp*fn)/(math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))))
				#print("Matthiews correlation coefficient (MCC) = ",mcc)

				#Balanced  Accuracy
				bacc = (((tp/(tp+tn))+(tn/(fp+fn)))/2)






	#write_scoring_file.close()

			
			csv_writer.writerow([f,str(args),str(tp),str(tn),str(fp),str(fn),str(pre),str(rec),str(acc),str(bacc),str(mcc)])
	csv_file.close()
	"""