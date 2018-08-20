import sys
import subprocess
import os

from subprocess import call

#Directory, where .py-script is stored

#Run CSV2TXT.R
dir = input("Please enter the directory to the CSV2TXT.R file \"/home/.../\":")

#Go to directory where the r-script is stored: "/home/nina/Schreibtisch/Masterarbeit/Scripte_R/"

r_parameter = "/usr/bin/Rscript --vanilla "+dir+"CSV2TXT.r"
csv2txt = subprocess.call (r_parameter, shell=True)
print("Thank you! All CSV file have been succesfully transformed and are stored in \"../TS2B/exapmles\"")

##### Or: in the Bash-file: Rscript CSV2TXT.r
