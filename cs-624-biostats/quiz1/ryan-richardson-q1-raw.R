library(ggplot2)
library(tidyr)
library(MASS)
mpgData = mpg
summary(mpgData)
head(mpgData)

mpgData$manufacturer = as.factor(mpgData$manufacturer)
mpgData$model = as.factor(mpgData$model)
mpgData$cyl = as.factor(mpgData$cyl)
mpgData$drv = as.factor(mpgData$drv)
mpgData$fl = as.factor(mpgData$fl)
mpgData$class = as.factor(mpgData$class)
mpgData$trans = as.factor(mpgData$trans)


mpgData$avgMpg = (mpgData$cty + mpgData$hwy) / 2
mpgData = mpgData[, !names(mpgData) %in% c("cty", "hwy")]


names(mpgData)
dim(mpgData)
summary(mpgData)

lModInteractions = lm(formula = avgMpg ~ model + displ + year + cyl + fl, data = mpgData)

stepModInteractions = stepAIC(lModInteractions, direction="both")

summary(stepModInteractions)



