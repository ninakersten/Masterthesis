#inputfile: /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV/
#outputfile: /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV2TXT_output
#install pandas
#!/usr/bin/python
import sys
import csv
import argparse
import os.path
import re

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Wrong input.")
		sys.exit()
	csv_input = sys.argv[1]
	#print(csv_input)

	#name_of_outputfile = ' '.join(sys.argv[1:])
	#print(name_of_outputfile)
	name_of_outputfile3 = csv_input.split('/')
	#print(name_of_outputfile3)
	name_of_outputfile1 = name_of_outputfile3[2].replace('.csv','')
	#print(name_of_outputfile1)

	r = csv.reader(open(csv_input))
	lines = list(r)
	#print(lines)
	line=lines[1]

	#get Antiboby names
	names = len(line[4:])
	#print(names)

	#Create first header
	names2= line[4:]
	namelist=list(names2)
	non_list=[]
	non_list.append('#NON')
	names3=non_list+names2
	#print(names3)

	symbollist = ["$","%","+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";","<",">","?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","_","`","~"]

	#create second header
	non_list1 =[]
	symbols = symbollist[0:(len(names2))]
	non_list1.append('NON')
	names4=non_list1+symbols

	#print(lines[4])
	#filtered_super_list=[]
	#for i in range(0,len(lines)):
	#	newlist9=lines[i]
	#	filtered_super_list1=[]
	#	for j,v in enumerate(lines[i]):
	#		newlist8= newlist9[j]
	#		newlist8=v.replace('0min','0').replace('5min','5')
	#filtered_super_list1.append(newlist8)
	#filtered_super_list.append(filtered_super_list1)
	#print(filtered_super_list)
		#if i[4]=='0min':
		#	print(i[4])


	filtered_list_Insulin =[]
	filtered_list_Serum =[]
	filtered_list_PBS =[]
	filtered_list_NRG1=[]
	filtered_list_IGF1=[]
	filtered_list_HGF=[]
	filtered_list_FGF1=[]
	filtered_list_EGF=[]
	for i in range(4,len(lines)):
		stimulilist = ['Insulin', 'Serum', 'PBS','NRG1', 'IGF1','HGF','FGF1', 'EGF','']
		newlist=lines[i]
		if newlist[2]==stimulilist[0]:
			filtered_list_Insulin.append(newlist)
		elif newlist[2]==stimulilist[1]:
			filtered_list_Serum.append(newlist)
		elif newlist[2]==stimulilist[2]:
			filtered_list_PBS.append(newlist)
		elif newlist[2]==stimulilist[3]:
			filtered_list_NRG1.append(newlist)
		elif newlist[2]==stimulilist[4]:
			filtered_list_IGF1.append(newlist)
		elif newlist[2]==stimulilist[5]:
			filtered_list_HGF.append(newlist)
		elif newlist[2]==stimulilist[6]:
			filtered_list_FGF1.append(newlist)
		elif newlist[2]==stimulilist[7]:
			filtered_list_EGF.append(newlist)
		elif newlist[2]==stimulilist[8]:
			filtered_list_Insulin.append(newlist)
			filtered_list_Serum.append(newlist)
			filtered_list_PBS.append(newlist)
			filtered_list_NRG1.append(newlist)
			filtered_list_IGF1.append(newlist)
			filtered_list_HGF.append(newlist)
			filtered_list_FGF1.append(newlist)
			filtered_list_EGF.append(newlist)
		#elif newlist[4]=='0min':
		#	replaced_list= newlist[4]
		#	replaced_list.replace('0min','')


	#timelist=[filtered_list_Insulin, filtered_list_Serum, filtered_list_PBS, filtered_list_NRG1, filtered_list_IGF1, filtered_list_HGF, filtered_list_FGF1, filtered_list_EGF]
	#for g in timelist:
	#for h in filtered_list_Serum:
	#	g=h[3]
	#		g.replace('0min','0')
	#print(filtered_list_Serum)

	filtered_list2_Insulin=[]
	for f in filtered_list_Insulin:
		filter1= f[3:]
		filtered_list2_Insulin.append(filter1)

	#newname = ' '.join(sys.argv[1:])
	#outputfile = newname.replace('./CSV_realdata/','').replace('.csv','Insulin')
	#filename ='{}.txt'.format(outputfile)
	filename= name_of_outputfile1 +'Insulin.txt'
	save_path = './CSV_realdata_2_TXT/'
	completeName = os.path.join(save_path, filename) 
	write_csv_file = open(completeName, "w")
	write_csv_file.write(' '.join(names4)+'\n')
	write_csv_file.write('\t'.join(names3)+'\n')
	for i in range(0,len(filtered_list_Insulin)):
				write_csv_file.write('\t'.join(filtered_list2_Insulin[i])+'\n')

	write_csv_file.close()

	filtered_list2_Serum=[]
	for f in filtered_list_Serum:
		filter1= f[3:]
		filtered_list2_Serum.append(filter1)

	#newname = ' '.join(sys.argv[1:])
	#outputfile = newname.replace('./CSV_realdata/','').replace('.csv','Serum')
	#filename ='{}.txt'.format(outputfile)
	filename=name_of_outputfile1 + 'Serum.txt'
	save_path = './CSV_realdata_2_TXT/'
	completeName = os.path.join(save_path, filename) 
	write_csv_file = open(completeName, "w")
	write_csv_file.write(' '.join(names4)+'\n')
	write_csv_file.write('\t'.join(names3)+'\n')
	for i in range(0,len(filtered_list_Serum)):
				write_csv_file.write('\t'.join(filtered_list2_Serum[i])+'\n')

	write_csv_file.close()


	filtered_list2_PBS=[]
	for f in filtered_list_PBS:
		filter1= f[3:]
		filtered_list2_PBS.append(filter1)

	#newname = ' '.join(sys.argv[1:])
	#outputfile = newname.replace('./CSV_realdata/','').replace('.csv','PBS')
	#filename ='{}.txt'.format(outputfile)
	filename = name_of_outputfile1 + 'PBS.txt'
	save_path = './CSV_realdata_2_TXT/'
	completeName = os.path.join(save_path, filename) 
	write_csv_file = open(completeName, "w")
	write_csv_file.write(' '.join(names4)+'\n')
	write_csv_file.write('\t'.join(names3)+'\n')
	for i in range(0,len(filtered_list_PBS)):
				write_csv_file.write('\t'.join(filtered_list2_PBS[i])+'\n')

	write_csv_file.close()


	filtered_list2_NRG1=[]
	for f in filtered_list_NRG1:
		filter1= f[3:]
		filtered_list2_NRG1.append(filter1)

	#newname = ' '.join(sys.argv[1:])
	#outputfile = newname.replace('./CSV_realdata/','').replace('.csv','NRG1')
	#filename ='{}.txt'.format(outputfile)
	filename = name_of_outputfile1 + 'NRG1.txt'
	save_path = './CSV_realdata_2_TXT/'
	completeName = os.path.join(save_path, filename) 
	write_csv_file = open(completeName, "w")
	write_csv_file.write(' '.join(names4)+'\n')
	write_csv_file.write('\t'.join(names3)+'\n')
	for i in range(0,len(filtered_list_NRG1)):
				write_csv_file.write('\t'.join(filtered_list2_NRG1[i])+'\n')

	write_csv_file.close()



	filtered_list2_IGF1=[]
	for f in filtered_list_IGF1:
		filter1= f[3:]
		filtered_list2_IGF1.append(filter1)

	#newname = ' '.join(sys.argv[1:])
	#outputfile = newname.replace('./CSV_realdata/','').replace('.csv','IGF1')
	#filename ='{}.txt'.format(outputfile)
	filename=name_of_outputfile1 + 'IGF1.txt'
	save_path = './CSV_realdata_2_TXT/'
	completeName = os.path.join(save_path, filename) 
	write_csv_file = open(completeName, "w")
	write_csv_file.write(' '.join(names4)+'\n')
	write_csv_file.write('\t'.join(names3)+'\n')
	for i in range(0,len(filtered_list_IGF1)):
				write_csv_file.write('\t'.join(filtered_list2_IGF1[i])+'\n')

	write_csv_file.close()

	filtered_list2_HGF=[]
	for f in filtered_list_HGF:
		filter1= f[3:]
		filtered_list2_HGF.append(filter1)

	#newname = ' '.join(sys.argv[1:])
	#outputfile = newname.replace('./CSV_realdata/','').replace('.csv','HGF')
	#filename ='{}.txt'.format(outputfile)
	filename=name_of_outputfile1 + 'HGF.txt'
	save_path = './CSV_realdata_2_TXT/'
	completeName = os.path.join(save_path, filename) 
	write_csv_file = open(completeName, "w")
	write_csv_file.write(' '.join(names4)+'\n')
	write_csv_file.write('\t'.join(names3)+'\n')
	for i in range(0,len(filtered_list_HGF)):
				write_csv_file.write('\t'.join(filtered_list2_HGF[i])+'\n')

	write_csv_file.close()


	filtered_list2_FGF1=[]
	for f in filtered_list_FGF1:
		filter1= f[3:]
		filtered_list2_FGF1.append(filter1)

	#newname = ' '.join(sys.argv[1:])
	#outputfile = newname.replace('./CSV_realdata/','').replace('.csv','FGF1')
	#filename ='{}.txt'.format(outputfile)
	filename=name_of_outputfile1 + 'FGF1.txt'
	save_path = './CSV_realdata_2_TXT/'
	completeName = os.path.join(save_path, filename) 
	write_csv_file = open(completeName, "w")
	write_csv_file.write(' '.join(names4)+'\n')
	write_csv_file.write('\t'.join(names3)+'\n')
	for i in range(0,len(filtered_list_FGF1)):
				write_csv_file.write('\t'.join(filtered_list2_FGF1[i])+'\n')

	write_csv_file.close()

	filtered_list2_EGF=[]
	for f in filtered_list_EGF:
		filter1= f[3:]
		filtered_list2_EGF.append(filter1)

	#newname = ' '.join(sys.argv[1:])
	#outputfile = newname.replace('./CSV_realdata/','').replace('.csv','EGF')
	#filename ='{}.txt'.format(outputfile)
	filename=name_of_outputfile1 + 'EGF.txt'
	save_path = './CSV_realdata_2_TXT/'
	completeName = os.path.join(save_path, filename) 
	write_csv_file = open(completeName, "w")
	write_csv_file.write(' '.join(names4)+'\n')
	write_csv_file.write('\t'.join(names3)+'\n')
	for i in range(0,len(filtered_list_EGF)):
				write_csv_file.write('\t'.join(filtered_list2_EGF[i])+'\n')

	write_csv_file.close()