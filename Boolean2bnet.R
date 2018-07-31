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

end_bool <- which(boolean2bnet[,1] == "Solution")# search the position of "solution"
start_bool <- end_bool +1 # go to the position of the error value 
best_bool_number <- which.min(start_bool) #From all positions where an error value occures take the min error and its position

# Take the start of the new file at the best min errors position till the next solution found occurence
best_bool <- boolean2bnet[start_bool[best_bool_number]:end_bool[best_bool_number+1],]

# Delete unnecessary rows
deletelist <- c("Cycle","Reached","Solution")
best_bool <- best_bool[!grepl("Cycle", best_bool$V1),]
best_bool <- best_bool[!grepl("Reached", best_bool$V1),]
best_bool <- best_bool[!grepl("Solution", best_bool$V1),]
best_bool <- best_bool[-1,]
best_bool <- best_bool[!grepl("False", best_bool$V3),]
boolean2bnet2<- best_bool[!grepl("True", best_bool$V3),]

# Get only the Boolean rules

boolean2bnet2[boolean2bnet2 == "and"] = as.character("&")
boolean2bnet2[boolean2bnet2 == "or"] = "|"
boolean2bnet2[boolean2bnet2 == "not"] = as.character("!")
boolean2bnet2[boolean2bnet2 == "="] = ","

#Ersetze alle Buchstaben durch den Knotennamen
#Lese input-file.txt für TS2B als data frame ein
name2node <- read.table("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/PBS.txt", fill= TRUE, header= FALSE, stringsAsFactors = FALSE, comment.char = "") 
name2node2 <- as.character(as.vector(name2node[2,-1]))
symbollist <- c("!", "$", as.character("%"),"+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";", "?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", "_", "~") #All possible single characters working with the TS2B model
symbollist2 <- c("!*", "$*", as.character("%*"),"+*", "-*", ".*","0*","1*","2*","3*","4*","5*","6*","7*","8*","9*", ":*", ";*", "?*", "@*","A*","B*","C*","D*","E*","F*","G*","H*","I*","J*","K*", "L*", "M*","N*","O*","P*","Q*","R*","S*","T*","U*","V*","W*","X*","Y*","Z*", "_*", "~*") #All possible single characters  with "*" working with the TS2B model


for (i in symbollist){
  for (j in symbollist2){
      boolean2bnet2[boolean2bnet2 == i] = as.character(name2node2[which(symbollist == i)])
      boolean2bnet2[boolean2bnet2 == j] = as.character(name2node2[which(symbollist2 == j)])
      
  }
}

new <- as.data.frame(sapply(boolean2bnet2,gsub,pattern="\\.",replacement="_"))

write.table(new, file = "output2.bnet", quote = FALSE, row.names=FALSE, col.names = FALSE)






