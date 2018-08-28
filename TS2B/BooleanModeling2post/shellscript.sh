#!/bin/bash
#Go to the ./Pipeline directory
# Make the script executable: chmod 700 shellscript.sh
# Run this script by typing "bash shellscript.sh"

#Runs CSV2TXT.r and transforms all csv files into txt files for TS2B and stores the data in ./Pipeline/CSV2TXT_output

Rscript CSV2TXT.r

#Runs a python script looping through all CSV2TXT_output files and runs for each the TS2B
#change directory to ./BooleanModeling2post
cd ..

inputlist='./Pipeline/CSV2TXT_output/*.txt'
for inputlist in $inputlist
do 
	python BinInfer.py input=$inputlist bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3

done

#cd ./Pipeline/PyBoolNet-2.2.5/
#python3 InteractionGraph.py ./TS2B_output/TS2B_outputfile.bnet






