#import sys
#import praw
#import os

#def direction(dir):
	#dir = input("Please enter the directory to the ./CSV -folder:")
	#return dir
	#/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV/

#dir = input("Please enter the directory to the ./CSV -folder:")




#test.py
#import sys

#arg1 = sys.argv[1]
#arg2 = sys.argv[2]
#print arg1, arg2

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", help="display a square of a given number")
args = parser.parse_args()
print(args.square)
