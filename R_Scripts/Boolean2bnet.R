###### Boolean Model (TS2B-output) to .bnet-file format-Parser####written by Nina Kersten 2018

# R version 3.4.3
#pip3 install praw
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

#Ersetze alle Buchstaben durch den Knotennamen
#Lese input-file.txt für TS2B als data frame ein
name2node <- read.table("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/CSV2TXTOutput.txt", fill= TRUE, header= FALSE, stringsAsFactors = FALSE, comment.char = "") 
#name2node <- name2node[2,]
boolean2bnet2[boolean2bnet2 == "A*"] = name2node[2,2]
boolean2bnet2[boolean2bnet2 == "A"] = name2node[2,2]
boolean2bnet2[boolean2bnet2 == "B*"] = name2node[2,3]
boolean2bnet2[boolean2bnet2 == "B"] = name2node[2,3]
boolean2bnet2[boolean2bnet2 == "C*"] = name2node[2,4]
boolean2bnet2[boolean2bnet2 == "C"] = name2node[2,4]
boolean2bnet2[boolean2bnet2 == "D*"] = name2node[2,5]
boolean2bnet2[boolean2bnet2 == "D"] = name2node[2,5]
boolean2bnet2[boolean2bnet2 == "E*"] = name2node[2,6]
boolean2bnet2[boolean2bnet2 == "E"] = name2node[2,6]
boolean2bnet2[boolean2bnet2 == "F*"] = name2node[2,7]
boolean2bnet2[boolean2bnet2 == "F"] = name2node[2,7]
boolean2bnet2[boolean2bnet2 == "G*"] = name2node[2,8]
boolean2bnet2[boolean2bnet2 == "G"] = name2node[2,8]
boolean2bnet2[boolean2bnet2 == "H*"] = name2node[2,9]
boolean2bnet2[boolean2bnet2 == "H"] = name2node[2,9]
boolean2bnet2[boolean2bnet2 == "I*"] = name2node[2,10]
boolean2bnet2[boolean2bnet2 == "I"] = name2node[2,10]
boolean2bnet2[boolean2bnet2 == "J"] = name2node[2,11]
boolean2bnet2[boolean2bnet2 == "J*"] = name2node[2,11]
boolean2bnet2[boolean2bnet2 == "K"] = name2node[2,12]
boolean2bnet2[boolean2bnet2 == "K*"] = name2node[2,12]
boolean2bnet2[boolean2bnet2 == "L"] = name2node[2,13]
boolean2bnet2[boolean2bnet2 == "L*"] = name2node[2,13]
boolean2bnet2[boolean2bnet2 == "M"] = name2node[2,14]
boolean2bnet2[boolean2bnet2 == "M*"] = name2node[2,14]
boolean2bnet2[boolean2bnet2 == "N"] = name2node[2,15]
boolean2bnet2[boolean2bnet2 == "N*"] = name2node[2,15]
boolean2bnet2[boolean2bnet2 == "O"] = name2node[2,16]
boolean2bnet2[boolean2bnet2 == "O*"] = name2node[2,16]
boolean2bnet2[boolean2bnet2 == "P"] = name2node[2,17]
boolean2bnet2[boolean2bnet2 == "P*"] = name2node[2,17]
boolean2bnet2[boolean2bnet2 == "Q"] = name2node[2,18]
boolean2bnet2[boolean2bnet2 == "Q*"] = name2node[2,18]
boolean2bnet2[boolean2bnet2 == "R"] = name2node[2,19]
boolean2bnet2[boolean2bnet2 == "R*"] = name2node[2,19]
boolean2bnet2[boolean2bnet2 == "S"] = name2node[2,20]
boolean2bnet2[boolean2bnet2 == "S*"] = name2node[2,20]
boolean2bnet2[boolean2bnet2 == "T*"] = name2node[2,21]
boolean2bnet2[boolean2bnet2 == "T"] = name2node[2,21]
boolean2bnet2[boolean2bnet2 == "U*"] = name2node[2,22]
boolean2bnet2[boolean2bnet2 == "U"] = name2node[2,22]
boolean2bnet2[boolean2bnet2 == "V*"] = name2node[2,23]
boolean2bnet2[boolean2bnet2 == "V"] = name2node[2,23]
boolean2bnet2[boolean2bnet2 == "W*"] = name2node[2,24]
boolean2bnet2[boolean2bnet2 == "W"] = name2node[2,24]
boolean2bnet2[boolean2bnet2 == "X*"] = name2node[2,25]
boolean2bnet2[boolean2bnet2 == "X"] = name2node[2,25]
boolean2bnet2[boolean2bnet2 == "Y"] = name2node[2,26]
boolean2bnet2[boolean2bnet2 == "Y*"] = name2node[2,26]
boolean2bnet2[boolean2bnet2 == "Z*"] = name2node[2,27]
boolean2bnet2[boolean2bnet2 == "Z"] = name2node[2,27]

new <- as.data.frame(sapply(boolean2bnet2,gsub,pattern="\\.",replacement="_"))

#character <- as.data.frame(as.character(boolean2bnet2))
#for boolean2bnet2 ("A":"Z"){
#  if (boolean2bnet2 == "A"){
#   boolean2bnet2 = names2node[,2:ncol]
#  }
#    print("error")
#}
#boolean2bnet2$V1 <- sub("^[^[:graph:]]", "", boolean2bnet2$V1)
#boolean2bnet2$V1 <- sub("^[\\*-]", "", boolean2bnet2$V1)
# Nach erster Spalte lexikographisch ordnen
# Von oben nach unten Buchstaben lexikographisch ersetzen
write.table(new, file = "output2.bnet", quote = FALSE, row.names=FALSE, col.names = FALSE)
new2 <- read.table("output2.bnet", fill= TRUE, header= FALSE, stringsAsFactors = FALSE)






