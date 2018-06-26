####CSV to TXT-Parser####by Nina Kersten

#This R-Parser converts a .csv-file of a RPMA-Output to a .txt-file for inferring a boolean network with TS2B
#install.packages("feather")
#library(feather)
#install.packages("curl")
#library(curl)
#Troubleshooting: Enter into the terminal: sudo apt-get install libcurl4-openssl-dev
#package "rio"contains the function 'convert'
#install.packages("rio")
#library(rio)
#install.packages("dplyr")
#library(dplyr)
install.packages("tibble")
library(tibble)

#function(file.csv){
	#read-in the data, exlude SlideID, Antibody Name
	newdata <- read.csv(file="/home/nina/Schreibtisch/Masterarbeit/DREAM8-Breast-Cancer/Training data/experimental/experimental/CSV/BT20_main.csv", header=FALSE, skip = 2, sep = ",", dec = ".", stringsAsFactors = FALSE)

	#filter all measurements with the FGF1-stimuli
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "FGF1")
  newdata2 <- subset(newdata, V4 == "0min" | V3 == "FGF1") # Filter for all "0min" and "FGF1" entries
  end_CSV <- which(newdata2[,3] == "FGF1") # gibt alle positionen wieder wo ein "FGF1" steht
  newdata3 <- newdata2[newdata2[1:end_CSV +1],] # nimmt nur den Teil auf dem data frame, der bin "FGF1" endet
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "Insulin")
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "IGF1")
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "EGF")
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "HGF")
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "Serum")
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "NRG1")
  #newdata2 <- dplyr::filter(newdata, newdata[,3] == "PBS")
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
	
	names(newdata4)[1] <- "NON"
	newdata4[newdata4 == "HUGO ID"] = "#NON"

	split_newdata4 <- newdata4[,1:24]	# Hälfte der Tabelle um mit kleineren Datensatz zu üben.

	#split_newdata5 <- add_row(split_newdata4,V5 = 1 , V6 = 3 , .before = 1)
		
	#split_newdata4$V5[[1]] #Returns the value at a certain position in a dataframe
	split_newdata5 <- split_newdata4[rep(1:nrow(split_newdata4),each=2),] 
	split_newdata5$NON[[1]] = "NON" #Replace "#NON" by "NON"
	
	s <- LETTERS[seq(split_newdata5[1,2:ncol(split_newdata5)])]
	
	write.table(split_size, file = "/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/CSV2TXT.txt", quote = FALSE, row.names=FALSE, col.names = TRUE)
	newdata3 <- read.table(file="/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/examples/CSV2TXT.txt", fill= TRUE, header = T)
	#colnames(newdata) <- c("NAN", "A", "B")

	# verkleinert die Tabelle auf nur 10 Einträge
	#newdata[,11:48]<- list(NULL)

	#Speichert neue CSV-Datei
	#write.csv(newdata, '/home/nina/Schreibtisch/Masterarbeit/DREAM8-Breast-Cancer/Training data/experimental/experimental/CSV/BT20_main_edit.csv', row.names=FALSE, na="")
  #Converts the .csv to a .tsv
	#convert("/home/nina/Schreibtisch/Masterarbeit/DREAM8-Breast-Cancer/Training data/experimental/experimental/CSV/BT20_main.csv", "/home/nina/Schreibtisch/Masterarbeit/DREAM8-Breast-Cancer/Training data/experimental/experimental/CSV/BT20_main.tsv")

	#converts .tsv to a .txt for the TS2B network generating tool
#}

