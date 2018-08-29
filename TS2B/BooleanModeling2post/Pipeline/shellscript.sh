#!/bin/bash
#Go to the ./Pipeline directory
# Make the script executable: chmod 700 shellscript.sh
# Run this script by typing "bash shellscript.sh"

#Runs CSV2TXT.r and transforms all csv files into txt files for TS2B and stores the data in ./Pipeline/CSV2TXT_output

Rscript CSV2TXT.r

#Runs a python script looping through all CSV2TXT_output files and runs for each the TS2B
#change directory to ./BooleanModeling2post
cd ..

#Here is a loop, but the the system will be out of memory.I recommand to use a loop only on a cluster.

#inputlist='./Pipeline/CSV2TXT_output/*.txt'
#for input in $inputlist
#do 

echo "Enter the directory to your inputfile [e.g.:./Pipeline/CSV2TXT_output/cellCycle.txt]:"
read var1
python BinInfer.py input=$var1 bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3

#done

#Run InteractionGraph.py
cd ./Pipeline/PyBoolNet-2.2.5/
echo "Enter the directory to your inputfile [e.g.:./TS2B_output/cellCycle.bnet]:"
read input2
#inputlist2='./TS2B_output/*.bnet'
#for input2 in $inputlist2
#do
python3 InteractionGraph.py $input2
#done





