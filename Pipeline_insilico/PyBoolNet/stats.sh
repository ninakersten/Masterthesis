#! /bin/bash



MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%\t\t", $3*100/$2 }')
DISK=$(df -h | awk '$NF=="/"{printf "%s\t\t", $5}')
CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%\t\t\n", $(NF-2)}')
	
#end=$((SECONDS+3600))
#while [ $SECONDS -lt $end ]; do
for ts2b_input in ./CSV_insilico_2_TXT/*.txt;do
before=$(date +%s)
python BinInfer.py input=$ts2b_input bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3
after=$(date +%s)
echo "$MEMORY$DISK$CPU"
sleep 2
done
