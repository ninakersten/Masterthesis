#pip3 install praw
# R version 3.4.3 is used, written by Nina Kersten 2018
#install.packages("utils")
#install.packages("rPython")
#library (utils)
#library (rPython)

#run python tool to create networks
#python.load("BESTFIT.py")
#python BinInfer.py input=/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/cellCycle.txt bin-method=KM3 learn-method=BESTFIT maxscore=0.05 solutions=3 > output.txt

setwd("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/")

#read in the output of the python tool, transforming a .txt file into a dataframe
boolean2bnet <- read.table("output.txt", fill= TRUE, header= FALSE, stringsAsFactors = FALSE)
end_bool <- which(boolean2bnet[,1] == "Solution")

#At the position of "solution" go one step below to get the error value
#start_bool <- solution +1 
start_bool <- end_bool +1 

#From all positions where an error value occures take the min error and its position
best_bool_number <- which.min(start_bool) 

# Take the start of the new file at the best min errors position till the next solution found occurence
best_bool <- boolean2bnet[start_bool[best_bool_number]:end_bool[best_bool_number+1],]

# Delete unnecessary rows
best_bool <- best_bool[-nrow(best_bool),]
best_bool <- best_bool[-nrow(best_bool),]
best_bool <- best_bool[-nrow(best_bool),]
best_bool<- best_bool [-1,]

# Get only the Boolean rules
n <- nrow(best_bool)
split_size <- nrow(best_bool)/2
r <- rep(1:ceiling(n/split_size),each=split_size)[1:n]
p <- split(best_bool, r)
best_bool <- p[2]
write.table(best_bool, file = "output2.bnet", quote = FALSE, row.names=FALSE, col.names = FALSE)
boolean2bnet2 <- read.table("output2.bnet", fill= TRUE, header= FALSE, stringsAsFactors = FALSE)
boolean2bnet2[boolean2bnet2 == "and"] = as.character("&")
boolean2bnet2[boolean2bnet2 == "or"] = "|"
boolean2bnet2[boolean2bnet2 == "not"] = as.character("!")
boolean2bnet2[boolean2bnet2 == "="] = ","
boolean2bnet2[boolean2bnet2 == as.character("A*")] = "A"
boolean2bnet2[boolean2bnet2 == as.character("B*")] = "B"
boolean2bnet2[boolean2bnet2 == as.character("C*")] = "C"
boolean2bnet2[boolean2bnet2 == as.character("D*")] = "D"
boolean2bnet2[boolean2bnet2 == as.character("E*")] = "E"
boolean2bnet2[boolean2bnet2 == as.character("F*")] = "F"
boolean2bnet2[boolean2bnet2 == as.character("G*")] = "G"
boolean2bnet2[boolean2bnet2 == as.character("H*")] = "H"
boolean2bnet2[boolean2bnet2 == as.character("I*")] = "I"
#boolean2bnet2$V1 <- sub("^[^[:graph:]]", "", boolean2bnet2$V1)
#boolean2bnet2$V1 <- sub("^[\\*-]", "", boolean2bnet2$V1)
# Nach erster Spalte lexikographisch ordnen
# Von oben nach unten Buchstaben lexikographisch ersetzen
write.table(boolean2bnet2, file = "output2.bnet", quote = FALSE, row.names=FALSE, col.names = FALSE)
boolean2bnet2 <- read.table("output2.bnet", fill= TRUE, header= FALSE, stringsAsFactors = FALSE)






