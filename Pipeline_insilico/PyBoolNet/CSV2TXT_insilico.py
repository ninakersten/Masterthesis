#inputfile: /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV/
#outputfile: /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV2TXT_output
#install pandas
#!/usr/bin/python
import sys
import csv
import argparse
import pandas
import os.path
import pandas as pd
#Pipeline$ python3 CSV2TXT.py ./CSV/

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Enter the directory of the ./TS2B_output/output2.bnet -file")
args = parser.parse_args()
#print(args)


r = csv.reader(open(args.dir))
lines = list(r)
line=lines[1]
names = len(line[4:])
#print(names)


filtered_list = []
for i in range(4,len(lines)):# insert args from bash: 100 timepoints '+4'
	newlist = lines[i]
	if newlist[2]=='Insulin':
		filtered_list.append(newlist)
	elif newlist[2]=='':
		filtered_list.append(newlist)
		continue
#print(filtered_list)

filtered_list2=[]
for f in filtered_list:
	filter1= f[3:]
	filtered_list2.append(filter1)

#print(filtered_list2)	


names2= line[4:]
namelist=list(names2)
non_list=[]
non_list.append('#NON')
names3=non_list+names2
#print(names3)


symbollist = ["$","%","+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";","<",">","?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","_","`","~"]

non_list1 =[]
symbols = symbollist[0:(len(names2))]
non_list1.append('NON')
names4=non_list1+symbols
#print(names4)




#for y in range(0,len(names2)

#write new csv.file
#with open('./CSV_insilico_2_TXT/Gold_4_13_10_2018_12_29.csv', mode='w') as csv_file:
#		csv_writer = csv.writer(csv_file, delimiter =',', quotechar ='"', quoting=csv.QUOTE_MINIMAL)
#		#Insert header: NON symbollist = ["$","%","+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";","<",">","?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","_","`","~"]
#		csv_writer.writerow(names4)
#		csv_writer.writerow(names3)
#		for i in range(0,100):#Problem beim richtigen Datensatz: Hier args einfügen from bash: create_continous_data.py
#			csv_writer.writerow(filtered_list2[i])
newname = ' '.join(sys.argv[1:])
outputfile = newname.replace('./CSV_insilico/','').replace('.csv','')
filename ='{}.txt'.format(outputfile)
save_path = './CSV_insilico_2_TXT/'
completeName = os.path.join(save_path, filename) 

write_csv_file = open(completeName, "w")

write_csv_file.write(' '.join(names4)+'\n')
write_csv_file.write('\t'.join(names3)+'\n')
for i in range(0,100):#Problem beim richtigen Datensatz: Hier args einfügen from bash: create_continous_data.py
			write_csv_file.write('\t'.join(filtered_list2[i])+'\n')


write_csv_file.close()

