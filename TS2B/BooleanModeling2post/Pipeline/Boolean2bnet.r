###### Boolean Model (TS2B-output) to .bnet-file format-Parser####written by Nina Kersten 2018

#R version 3.4.3 (2017-11-30)
#install.packages("utils")
#install.packages("rPython")
#library (utils)
#library (rPython)
#run python tool to create networks
#python.load("BESTFIT.py")
#python BinInfer.py input=/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/cellCycle.txt bin-method=KM3 learn-method=BESTFIT maxscore=0.05 solutions=3 > output.txt

#setwd("/home/nina/Schreibtisch/Masterarbeit/")
#Asking for directory of the input file and the output file
cat("Please enter the directory to the ./TS2B_output/[filename.txt] - output data:")
#/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/TS2B_output/output.txt
fil3 <- readLines(con="stdin", 1)
askdir3 <- cat(fil3, "\n")

#reading .txt-file with a variable number of coloumns
no_col <- max(count.fields(fil3, sep = " "))
boolean2bnet <- read.table(fil3,sep=" ",fill=TRUE,header = F,stringsAsFactors = FALSE, col.names=c(1:no_col))


end_bool <- which(boolean2bnet[,1] == "Solution")# search the position of "solution"
start_bool <- end_bool +1 # go to the position of the error value 
best_bool_number <- which.min(start_bool) #From all positions where an error value occures take the min error and its position

# Take the start of the new file at the best min errors position till the next solution found occurence
best_bool <- boolean2bnet[start_bool[best_bool_number]:end_bool[best_bool_number+1],]

# Delete unnecessary rows
deletelist <- c("Cycle","Reached","Solution")
best_bool <- best_bool[!grepl("Cycle", best_bool[,1]),]
best_bool <- best_bool[!grepl("Reached", best_bool[,1]),]
best_bool <- best_bool[!grepl("Solution", best_bool[,1]),]
best_bool <- best_bool[-1,]
best_bool <- best_bool[!grepl("False", best_bool[,3]),]
boolean2bnet2<- best_bool[!grepl("True", best_bool[,3]),]

# Replace boolean expressions

boolean2bnet2[boolean2bnet2 == "and"] = as.character("&")
boolean2bnet2[boolean2bnet2 == "or"] = "|"
boolean2bnet2[boolean2bnet2 == "not"] = as.character("!")
boolean2bnet2[boolean2bnet2 == "="] = ","

#Read in the CSV2TXT validated outputfile such that the protein's names can be added to the boolean rules

cat("Please enter the directory to the .CSV2TXT_output/[csv2txt_output_filename_fitting to the TS2B_output_file].txt -file:")
# /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV2TXT_output/BT20_mainEGF.txt
fil5 <- readLines(con="stdin", 1)
askdir5 <- cat(fil5, "\n")

name2node <- read.table(fil5, fill= TRUE, header= FALSE, stringsAsFactors = FALSE, comment.char = "") 
#Transform the protein's names into a vector
name2node2 <- as.character(as.vector(name2node[2,-1]))
#Create a vector of all possible character's encoding a protein (limited by TS2B in /boolean2/tokenizer.py)
symbollist <- c("$", as.character("%"),"+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";","<",">","?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","_","`","~") #All possible single characters working with the TS2B model
symbollist2 <- c("$*", as.character("%*"),"+*", "-*", ".*","0*","1*","2*","3*","4*","5*","6*","7*","8*","9*", ":*", ";*","<*",">*","?*", "@*","A*","B*","C*","D*","E*","F*","G*","H*","I*","J*","K*", "L*", "M*","N*","O*","P*","Q*","R*","S*","T*","U*","V*","W*","X*","Y*","Z*","_*","`*","~*") #All possible single characters  with "*" working with the TS2B model

for (i in symbollist){
  for (j in symbollist2){
    boolean2bnet2[boolean2bnet2 == i] = as.character(name2node2[which(symbollist == i)])
    boolean2bnet2[boolean2bnet2 == j] = as.character(name2node2[which(symbollist2 == j)])
    
  }
}


#In case of PyBoolNet: Replace all "." in a protein's name by "_", because in PyBoolNet "." in a protein's name cause trouble
boolean2bnet2 <- as.data.frame(sapply(boolean2bnet2,gsub,pattern="\\.",replacement="__"))
#write.table(new, file = "output2.bnet", quote = FALSE, row.names=FALSE, col.names = FALSE, sep = " ")

cat("Please enter the directory to the ./Pipeline/PyBoolNet-2.2.5/ -folder:")
#/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/
fil4 <- readLines(con="stdin", 1)
askdir4 <- cat(fil4, "\n")

#setwd("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/PyBoolNet-2.2.5/")
write.table(boolean2bnet2, file = paste(fil4,"output2.bnet", sep = ""), quote = FALSE, row.names=FALSE, col.names = FALSE, sep = " ")

