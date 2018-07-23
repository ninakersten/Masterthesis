####CSV to TXT-Parser####by Nina Kersten

#This R-Parser converts a .csv-file of a RPMA-Output to a .txt-file for inferring a boolean network with TS2B

#install.packages("ddR")
#install.packages("plyr")
#library(ddR)
#library(plyr)


### Creating the 1. Stimuli-Dataset: "FGF1"###
	#read-in the data, exlude SlideID, Antibody Name
	newdata <- read.csv(file="/home/nina/Schreibtisch/Masterarbeit/DREAM8-Breast-Cancer/Training data/experimental/experimental/CSV/BT20_main.csv", header=FALSE, skip = 2, sep = ",", dec = ".", stringsAsFactors = FALSE)

	#filter all measurements with the FGF1-stimuli
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "FGF1")
  #newdata2 <- subset(newdata, V4 == "0min" | V3 == "FGF1") # Filter for all "0min" and "FGF1" entries
  #newdata2 <- subset(newdata, V4 == "0min" | V3 == "Insulin") # Filter for all "0min" and "Insulin" entries
  #newdata2 <- subset(newdata, V4 == "0min" | V3 == "IGF1")
  #newdata2 <- subset(newdata, V4 == "0min" | V3 == "EGF")
  #newdata2 <- subset(newdata, V4 == "0min" | V3 == "HGF")
  #newdata2 <- subset(newdata, V4 == "0min" | V3 == "Serum")
  #newdata2 <- subset(newdata, V4 == "0min" | V3 == "NRG1")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "PBS")
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "Insulin")
  #end_CSV <- which(newdata2[,3] == "FGF1") # gibt alle positionen wieder wo ein "FGF1" steht
  #end_CSV <- which(newdata2[,3] == "Insulin") # gibt alle positionen wieder wo ein "FGF1" steht
  #newdata3 <- newdata2[newdata2[1:end_CSV +1],] # nimmt nur den Teil auf dem data frame, der bin "FGF1" endet

  newdata3 <- newdata[1,]	
  newdata2$V1 <- NULL
	newdata2$V2 <- NULL
	newdata2$V3 <- NULL
	newdata3$V1 <- NULL
	newdata3$V2 <- NULL
	newdata3$V3 <- NULL
	#Problem: die 0min.-Werte fehlen
	#exlude coloumns like Cell Line, Inhibitor, Stimulus

	newdata2[newdata2 == "0min"] = 0
	newdata2[newdata2 == "5min"] = 5
	newdata2[newdata2 == "10min"] = 10
	newdata2[newdata2 == "15min"] = 15
	newdata2[newdata2 == "30min"] = 30
	newdata2[newdata2 == "60min"] = 60
	newdata2[newdata2 == "2hr"] = 120
	newdata2[newdata2 == "4hr"] = 240
	
	#Verbinde wieder newdata2 mit newdata3:
	newdata4 <- rbind(newdata3, newdata2) 
	
	#names(newdata4)[1] <- "NON"
	newdata4[newdata4 == "HUGO ID"] = "#NON"

	split_newdata4 <- newdata4[,1:20]	# Hälfte der Tabelle um mit kleineren Datensatz zu üben.Sonst gibt es zu viele Knoten und zu wenig Messpunkte.

	#split_newdata5 <- add_row(split_newdata4,V5 = 1 , V6 = 3 , .before = 1)
		
	#split_newdata4$V5[[1]] #Returns the value at a certain position in a dataframe
	#split_newdata5 <- split_newdata4[rep(1:nrow(split_newdata4),each=2),] 
	#split_newdata5$NON[[1]] = "NON" #Replace "#NON" by "NON"
	
	
  # Replace ID by "A-Z" in the first row of the data frame
	a <- c("NON",LETTERS[seq(split_newdata4[1,2:ncol(split_newdata4)])])
	b <- (paste(a , collapse =" "))
	c <- as.data.frame(b)
	d <- rbind.fill(c, split_newdata4)
  d[1,2] <- as.character(d[1,1])
  d$b <- NULL
  d[is.na(d)] <- ""
	
  setwd("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/")
	write.table(d, file = "CSV2TXTOutput.txt", quote = FALSE, row.names=FALSE, col.names = FALSE)
	
	
	
	
	
	#newdata5 <- read.table(file="CSV2TXTOutput.txt", fill= TRUE, header = F)
	
	# add "NON" in first entry to get the same dimension as split_newdata5
  #x <- t(newdata3)
	# transpose the list and convert it into a dataframe 
  #converted_data <- data.frame(as.list(t(newdata5)))
  # equalize the names of the rows
  #names(converted_data) = names (split_newdata4)

  #names(converted_data) == names (split_newdata4) # check Equalization
  # Merge the dataframe of the char-header with A-Z with the oroginal data, to get two header
  Data <- rbind(converted_data,split_newdata4)
  

  

  #take all letters into the first [1,1] entry of the dataframe
 

  write.table(Data2, file = "/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/CSV2TXTOutput.txt", quote = FALSE, row.names=FALSE, col.names = FALSE, sep = "\t")
  
  

