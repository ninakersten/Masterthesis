####CSV to TXT-Parser####by Nina Kersten

#This R-Parser converts a .csv-file of a RPMA-Output to a .txt-file for inferring a boolean network with TS2B
#Up to 48 nodes can be calculated

#install.packages("plyr")
#install.packages("data.table") #data.table_1.9.5
library(plyr)
library(data.table) 


### Creating the 1. Stimuli-Dataset: "FGF1"###
	#read-in the data, exlude SlideID, Antibody Name
	newdata <- read.csv(file="/home/nina/Schreibtisch/Masterarbeit/DREAM8-Breast-Cancer/Training data/experimental/experimental/CSV/BT20_main.csv", header=FALSE, skip = 2, sep = ",", dec = ".", stringsAsFactors = FALSE)

	#filter all measurements with the FGF1-stimuli
	
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "FGF1")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "Insulin")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "IGF1")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "EGF")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "HGF")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "Serum")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "NRG1")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "PBS")

  
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

	#split_newdata4 <- newdata4[,1:39]	# Hälfte der Tabelle um mit kleineren Datensatz zu üben.Sonst gibt es zu viele Knoten und zu wenig Messpunkte.
	split_newdata4 <- newdata4# mit normaler Datensatzgröße weiterabeiten
	#split_newdata5 <- add_row(split_newdata4,V5 = 1 , V6 = 3 , .before = 1)
		
	#split_newdata4$V5[[1]] #Returns the value at a certain position in a dataframe
	#split_newdata5 <- split_newdata4[rep(1:nrow(split_newdata4),each=2),] 
	#split_newdata5$NON[[1]] = "NON" #Replace "#NON" by "NON"
	

	

  e <- c("!", "$", as.character("%"),"+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";", "?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z", "_", "~")
  g <- c("NON", e[1:ncol(split_newdata4)-1])
  b <- (paste(g, collapse =" "))
  c <- as.data.frame(b)
  f <- rbind.fill(list(c,split_newdata4))
  f[1,2] <- as.character(f[1,1])
  f$b <- NULL
  f[is.na(f)] <- ""
  
  setwd("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/")
	write.table(f, file = "CSV2TXTOutput.txt", quote = FALSE, row.names=FALSE, col.names = FALSE)

