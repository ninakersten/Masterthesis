import sys
import csv
import argparse
import pandas
import os.path
#Pipeline$ python3 CSV2TXT.py ./CSV/
if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Wrong input.")
		sys.exit()
	csv_input = sys.argv[1]
	print(csv_input)

	#name_of_outputfile = ' '.join(sys.argv[1:])
	#print(name_of_outputfile)
	name_of_outputfile3 = csv_input.split('/')
	print(name_of_outputfile3)
	name_of_outputfile1 = name_of_outputfile3[2].replace('.csv','')
	print(name_of_outputfile1)