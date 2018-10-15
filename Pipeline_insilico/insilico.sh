#!/bin/bash
# Run from 'homedirectory'
# Go to the ./Pipeline_insilico/
# Make the script executable: chmod 700 shellscript.sh
# Run this script by typing:
# bash insilico.sh 'number of max. nodes' 'number of measurements' 'binarization-method' 'inference-algorithm'
#e.g: bash insilico.sh 7 150 KM3 BESTFIT

###Create a inlisico_bnet_data set###

#Besser: parameterfiles nicht mit ausgeben
#Rausfinden: Welche Boolschen Regeln einen Konflikt ergeben?

#echo "What is the maximum number of nodes an insilico network should have? Start at least by a value of 5 ! (e.g.10)"
#	read nodes

python3 create_bnet_data.py $1

#echo "You can find the resulting bnet-files in ./PyBoolNet/bnet_data_insilico/ !"

cd ./PyBoolNet/

#Create insilico-goldstandard-sif files

for input in ./bnet_data_insilico/Gold_*.bnet; do
	python3 InteractionGraph_insilico_gold.py $input
done

#echo "You can find the resulting bnet-files in ./PyBoolNet/goldstandard_insilico/ !"

#Create continous data with odefy
cd ..


for input2 in ./PyBoolNet/bnet_data_insilico/Gold_*.bnet; do
	#echo "How many timepoints should the continous data set have? 		#(e.g: 100,120, 130....200)"
	#read timepoints

#	python3 create_continuous_data.py $input2 $input2 [0,50] $timepoints [1,5] [0.4,0.6] [1,3]


python3 create_continuous_data.py $input2 $input2 [0,50] $2 [1,5] [0.4,0.6] [1,3]


done

####Convert the .csv files to inpu_file-format of the inference algorithms####

#Problem: Homepfad ändert sich immer
#Bzeichner für scoring rausnehmen: 'Insulin' in der prediction

cd ./PyBoolNet/

for csv_input in ./CSV_insilico/*.csv;do

python3 CSV2TXT_insilico.py $csv_input

done


####Run inference algorithms and discretization algorithms###

#Zeitmessung erfassen und mit inputfilename speichern

for ts2b_input in ./CSV_insilico_2_TXT/*.txt; do
before=$(date +%s)
python BinInfer.py input=$ts2b_input bin-method=$3 learn-method=$4 maxscore=10.0 solutions=3
after=$(date +%s)
runtime=$((after - $before))
echo $runtime
done

#Problem:In BinInfer.py muss immer alles aus dem Namen gelöscht werden (daher zz. nur KM1-3,A und REVEAL,BESTFIT,FULLFIT möglich)


###Create Prediction .sif files###
# Bennene .sif file in Pred_xxx.sif um anstatt Gold_xxx.sif
for ts2b_output in ./inference_output_insilico/*.bnet; do
	python3 InteractionGraph_insilico_pred.py $ts2b_output

done
###Score Prediction against the goldstandard###

#python3 scoring.py $timepoints $binmethod $learnmethod

python3 scoring.py $2 $runtime
#python3 scoring.py $2 $runtime

###Make new directory for the results###
#This part saves all results of a run in a new directory and clears the initial directory s.t. a new run can be started.
cd ./Backup
newdir=$(date '+%d-%b-%Y-%H-%M-%S')

mkdir $newdir
cd ./$newdir

mkdir prediction_insilico inference_output_insilico goldstandard_insilico CSV_insilico_2_TXT CSV_insilico bnet_data_insilico

cd ..
cd ..

for newdir2 in ./prediction_insilico/*.sif;do
	mv -f -i $newdir2 ./Backup/$newdir/prediction_insilico
done
for newdir3 in ./goldstandard_insilico/*.sif;do
	mv -f -i $newdir3 ./Backup/$newdir/goldstandard_insilico
done
for newdir4 in ./inference_output_insilico/*.bnet;do
	mv -f -i $newdir4 ./Backup/$newdir/inference_output_insilico
done
for newdir5 in ./CSV_insilico_2_TXT/*.txt;do
	mv -f -i $newdir5 ./Backup/$newdir/CSV_insilico_2_TXT
done
for newdir6 in ./CSV_insilico/*.csv;do
	mv -f -i $newdir6 ./Backup/$newdir/CSV_insilico
done
for newdir7 in ./bnet_data_insilico/*.bnet;do
	mv -f -i $newdir7 ./Backup/$newdir/bnet_data_insilico
done
mv -f -i scoring_result.csv ./Backup/$newdir
