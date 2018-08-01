### bnet2sif.R ### written by Nina Kersten

# In this script the realationship of the protein-protein-interactions are provided
# The bnet-format shows the boolean rules for each node in the network
# Here the priority of the boolean operators is "!"-> "&" -> "|" (strong -> weak)
# e.g.(in .bnet): ProteinA* ,  ProteinB & !ProteinC | ProteinD
# e.g.(in .sif):  ProteinB  1 ProteinA
#                 ProteinC -1 ProteinA
#                 ProteinD  1 ProteinA
#Thus the AUROC-value can be calculated by DREAMTools

#R version 3.4.3 (2017-11-30)

setwd("/home/nina/Schreibtisch/Masterarbeit/Algorithmen/TS2B/BooleanModeling2post/")
bnet_data <- read.table("output2.bnet", fill= TRUE, header= FALSE, stringsAsFactors = FALSE, sep = " ")

proteinlist <- c(bnet_data[,1])
bnet_subdata <- bnet_data[,3:ncol(bnet_data)]
#index <- which(bnet_data == "EIF4EBP1_pT37_pT46", arr.ind=TRUE)

mybiglist <- list()

for (protein in proteinlist){
  
  indexlist <- which(bnet_subdata == protein, arr.ind=TRUE)
  name <- paste(protein,":",sep=" ")
  mybiglist[[name]] <- indexlist
  #print(index)
  
  #dir.create("/BnetData")
  #write.table(indexlist,paste(protein,sep = ".","txt"), sep="\t", quote = FALSE, row.names=FALSE, col.names = FALSE)
}


for (x in mybiglist){
  for(y in 1:nrow(mybiglist[[x]])){
    for(z in mybiglist[[y]]){
    if (bnet_subdata[y[1,],y[,1-1]] == "!"){
      
      print("Inactive")
      
    }else if(bnet_subdata[y[1,],y[,1-1]] == "|"){
      
      print("Active")
      }
    }
  }
}



