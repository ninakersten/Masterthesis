#!/bin/bash
# Run from 'homedirectory'
# Go to the ./Pipeline_insilico/
# Make the script executable: chmod 700 shellscript.sh
# Run this script by typing "bash insilico.sh"

###Create a inlisico_bnet_data set###

#Besser: parameterfiles nicht mit ausgeben
#Rausfinden: Welche Boolschen Regeln einen Konflikt ergeben?

echo "What is the maximum number of nodes an insilico network should have? Start at least by a value of 5 ! (e.g.10)"
	read nodes

python3 create_bnet_data.py $nodes

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

python3 create_continuous_data.py $input2 $input2 [0,50] 100 [1,5] [0.4,0.6] [1,3]


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
python BinInfer.py input=$ts2b_input bin-method=KM3 learn-method=REVEAL maxscore=10.0 solutions=3
after=$(date +%s)
echo "The time elapsed for" $ts2b_input ":" $((after - $before)) "seconds"

done


###Create Prediction .sif files###
# Bennene .sif file in Pred_xxx.sif um anstatt Gold_xxx.sif
for ts2b_output in ./inference_output_insilico/*.bnet; do
	python3 InteractionGraph_insilico_pred.py $ts2b_output

done
###Score Prediction against the goldstandard###


python3 scoring.py


