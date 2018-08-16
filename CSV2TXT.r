####CSV to TXT-Parser####by Nina Kersten

#This R-Parser converts a .csv-file of a RPMA-Output to a .txt-file for inferring a boolean network with TS2B
#Up to 48 nodes can be calculated

#R version 3.4.3 (2017-11-30)
#install.packages("plyr")
#install.packages("data.table") #data.table_1.9.5
library(plyr)

cat("Please enter the directory to the ./CSV/ -folder:")
fil <- readLines(con="stdin", 1)
askdir <- cat(fil, "\n")
#Example format: /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/Pipeline/CSV/

cat("Please enter the directory to the ./TS2B/BooleanModeling2post/ -folder:")
fil2 <- readLines(con="stdin", 1)
askdir <- cat(fil2, "\n")
#Example format: /home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/

setwd(fil2)
celllinelist <- c("BT20_main","BT549_main","MCF7_main","UACC812_main")
#read-in the data, exlude SlideID, Antibody Name
for (d in celllinelist){
newdata <- read.csv(file=paste(fil,d,".csv", sep=""), header=FALSE, skip = 2, sep = ",", dec = ".", stringsAsFactors = FALSE)
stimulilist<- c("Insulin", "IGF1", "FGF1", "EGF", "HGF" , "Serum", "NRG1" , "PBS") # List of all stimuli (pertubation parameter) used in the experiments in each cell line
 
   for (i in stimulilist){
    
     newdata2 <- subset(newdata, newdata$V4 == "0min" | newdata$V3 == i) # filter out the measurements of one cell line in combination with the 0-measurements and one of the pertubation parameters
      #newdata2 <- newdata[match(stimulilist, newdata), ]
      #newdata2 <- subset(newdata, newdata$V3 %in% stimulilist | newdata$V4== "0min")
      #newdata$V3 <- rownames(newdata)
      #newdata2 <- subset(newdata, V4 == "0min" | V3 == "Insulin")
      newdata3 <- newdata[1,]	
      newdata2$V1 <- NULL 
      newdata2$V2 <- NULL
      newdata2$V3 <- NULL
      newdata3$V1 <- NULL
      newdata3$V2 <- NULL
      newdata3$V3 <- NULL
      newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="min",replacement=" "))
      newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="2hr",replacement="120"))
      newdata2 <- as.data.frame(sapply(newdata2,gsub,pattern="4hr",replacement="240"))
      newdata4 <- rbind(newdata3, newdata2) # Combine the filtered dataset with the header of the antobodies names (names of the nodes in the network)
      newdata4[newdata4 == "HUGO ID"] = "#NON"
      split_newdata4 <- newdata4
      #split_newdata4 <- newdata4[,20]# Working with a smaller dataset
      e <- c("$", as.character("%"),"+", "-", ".","0","1","2","3","4","5","6","7","8","9", ":", ";","<",">","?", "@","A","B","C","D","E","F","G","H","I","J","K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","_","`","~") #All possible single characters working with the TS2B model
      g <- c("NON", e[1:ncol(split_newdata4)-1])
      #g <- c(i, "NON", e[1:ncol(split_newdata4)-1])# Control: Shows wether the loop works by putting (i) in the headerof the .txt-file
      b <- (paste(g, collapse =" "))
      c <- as.data.frame(b)
      f <- rbind.fill(list(c,split_newdata4))
      f[1,2] <- as.character(f[1,1])
      f$b <- NULL
      f[is.na(f)] <- ""
      
      
      # delete duplicated measurements
      #f2 <- f[!duplicated(f), ]
      
      #Rearrange the data by the time
      #h <- f[with(f, order(V4)),]
      #h <-as.data.frame(sort(f$V4, decreasing=T))
      #h <- f[3,order(f$V4)]
      
      #ndx = order(f$V4, decreasing=T)
      #f_sorted = f[ndx,]
      
      #ifelse(!dir.exists("CSV2TXTOutput"), dir.create("CSV2TXTOutput"), "Folder exists already") # Creates a folder for the output
      #write.table(f, file = paste(i,".txt"), sep="\t", quote = FALSE, row.names=FALSE, col.names = FALSE)
      write.table(f,paste(d,i,Sys.time(),sep = ".","txt"), sep="\t", quote = FALSE, row.names=FALSE, col.names = FALSE)
      
   }
}


