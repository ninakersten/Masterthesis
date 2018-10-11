#inputfile: /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV/
#outputfile: /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV2TXT_output
#install pandas
import sys
import csv
import argparse
import pandas
import os.path

#Pipeline$ python3 CSV2TXT.py ./CSV/

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Enter the directory of the ./CSV/- file")
args = parser.parse_args()

#print(args)

with open(args.dir) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	print(csv_reader)
	line_count = 0

#oder 
#df = pandas.read_csv(args.dir)

#print(df)

#filename ='TS2B_input.txt'
#file = open(filename, "w")
#file.write(df.to_string)