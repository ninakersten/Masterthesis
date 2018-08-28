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
for input in $inputlist
do 
	python BinInfer.py input=$input bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3

done

#Run InteractionGraph.py
cd ./Pipeline/PyBoolNet-2.2.5/
inputlist2='./TS2B_output/*.bnet'
for input2 in $inputlist2
do
	python3 InteractionGraph.py $input2
done





