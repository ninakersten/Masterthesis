import sys
import subprocess
import os

from subprocess import call

#Directory, where .py-script is stored

#Run CSV2TXT.R
dir = input("Please enter the directory to the CSV2TXT.R file \"/home/.../\":")

#Go to directory where the r-script is stored: "/home/nina/Schreibtisch/Masterarbeit/Scripte_R/"

r_parameter = "/usr/bin/Rscript --vanilla "+dir+"CSV2TXT.R"
csv2txt = subprocess.call (r_parameter, shell=True)
print("Thank you! All CSV file have been succesfully transformed and are stored in \"../TS2B/exapmles\"")


#Run TS2B


#Go to directory of BooleanModeling2post

if __name__ == '__main__':
	os.chdir("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post")
	os.system("pwd")
	os.system("/bin/bash")		

#os.chdir("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/")


call(["python", "BinInfer.py", "input=/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/Serum.txt", "bin-method=KM3", "learn-method=BESTFIT", "maxscore=10.0", "solutions=3", ">", "Stimuli_Output.txt"])

#ts2b_parameter = "python BinInfer.py input=/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/Serum.txt bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3 > Stimuli_Output.txt"
#subprocess.check_call(ts2b_parameter, shell=True)

#subprocess.check_call("python BinInfer.py input= "+dir2+" bin-method=KM3 learn-method=BESTFIT maxscore=10.0 solutions=3 > Stimuli_Output.txt")



#Run Boolean2Bnet.R
#r_parameter = "/usr/bin/Rscript --vanilla "+dir+"Boolean2bnet.R"
#csv2txt = subprocess.call (r_parameter, shell=True)
#print("Thank you! All Boolean rules from TS2B have been succesfully transformed into a .bnet-format and are stored in \"..\"")


#Run InteractionGraph.py to create the sif format



