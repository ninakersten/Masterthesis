#!/bin/bash
# Run from 'homedirectory'
# Go to the ./Pipeline_realdata/
# Make the script executable: chmod 700 shellscript.sh
# Run this script by typing:
# bash realdata.sh 'binarization-method' 'inference-algorithm'
#e.g: bash realdata.sh KM3 BESTFIT

####Convert the .csv files to inpu_file-format of the inference algorithms####

#Bzeichner für scoring rausnehmen: 'Insulin' in der prediction

cd ./PyBoolNet/

for csv_input in ./CSV_realdata/*.csv;do

python3 CSV2TXT_realdata.py $csv_input

#example: python3 CSV2TXT_realdata.py ./CSV_realdata/BT20_main.csv
#Problem: In den /CSV_realdata/*.csv-files musste '0min' manuellreplaced werden!
done


####Run inference algorithms and discretization algorithms###

#Zeitmessung erfassen und mit inputfilename speichern

for ts2b_input in ./CSV_realdata_2_TXT/*.txt; do
before=$(date +%s)
python BinInfer.py input=$ts2b_input bin-method=$1 learn-method=$2 maxscore=10.0 solutions=3
after=$(date +%s)
runtime=$((after - $before))
echo $ts2b_input  $runtime
done > runtime.txt

#example:
#python BinInfer.py input=./CSV_realdata_2_TXT/BT20_mainSerum.txt bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3

#Problem:In BinInfer.py muss immer alles aus dem Namen gelöscht werden (daher zz. nur KM1-3,A und REVEAL,BESTFIT,FULLFIT möglich)

###Create Prediction .sif files###
# Bennene .sif file in Pred_xxx.sif um anstatt Gold_xxx.sif
for ts2b_output in ./inference_output_realdata/*.bnet; do
	python3 InteractionGraph_realdata_pred.py $ts2b_output

done
###Score Prediction against the goldstandard###

#python3 scoring.py $timepoints $binmethod $learnmethod

python3 scoring.py $3 $4

#Vielleicht noch die Anzahl der measurements hinzufügen?

###Make new directory for the results###
#This part saves all results of a run in a new directory and clears the initial directory s.t. a new run can be started.
cd ./Backup
newdir=$(date '+%d-%b-%Y-%H-%M-%S')

mkdir $newdir
cd ./$newdir

mkdir prediction_realdata inference_output_realdata goldstandard_realdata CSV_realdata_2_TXT CSV_realdata bnet_data_realdata
cd ..
cd ..
for newdir2 in ./goldstandard_realdata/*.sif;do
	cp -f -i $newdir2 ./Backup/$newdir/goldstandard_realdata
done
for newdir3 in ./inference_output_realdata/*.bnet;do
	mv -f -i $newdir3 ./Backup/$newdir/inference_output_realdata
done
for newdir4 in ./prediction_realdata/*.sif;do
	mv -f -i $newdir4 ./Backup/$newdir/prediction_realdata
done
for newdir5 in ./CSV_realdata_2_TXT/*.txt;do
	mv -f -i $newdir5 ./Backup/$newdir/CSV_realdata_2_TXT
done
for newdir6 in ./CSV_realdata/*.csv;do
	cp -f -i $newdir6 ./Backup/$newdir/CSV_realdata
done
mv -f -i scoring_result.csv ./Backup/$newdir
mv -f -i runtime.txt ./Backup/$newdir
