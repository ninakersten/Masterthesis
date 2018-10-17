

install.packages("PRROC")
library(PRROC)

scoring <- read.csv(file='scoring_result.csv', header=FALSE, sep = ",", dec = ".", stringsAsFactors = FALSE)

require(PRROC)
fg <- probs[df$label == 1]
bg <- probs[df$label == 0]

# ROC Curve    
roc <- roc.curve(scores.class0 = fg, scores.class1 = bg, curve = T)
plot(roc)

# PR Curve
pr <- pr.curve(scores.class0 = fg, scores.class1 = bg, curve = T)
plot(pr)