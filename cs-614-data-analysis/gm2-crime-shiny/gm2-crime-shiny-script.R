library(tidyverse)
library(dplyr)
library(reshape2)
crimeData = read.csv('UOF_BY_DEPARTMENTS.csv', head=TRUE)
factorCols <- c("Town_county","pd_dept_plus_county","pd_dept","county","coverage_city")

crimeData[factorCols] <- lapply(crimeData[factorCols], factor)

crimeDataMin = data.frame(
  "WhitePopulation"= crimeData$pctwhite_adjpop, "BlackPopulation"= crimeData$pctblack_adjpop, "HispanicPopulation"= crimeData$pcthisp_adjpop, "AsianPacificPopulation"= crimeData$pctasian_adjpop,
  "WhiteOfficers"= crimeData$white_pct_officers, "BlackOfficers"= crimeData$black_pct_officers, "HispanicOfficers"= crimeData$hispanic_pct_officers, "AsianPacificOfficers"= crimeData$asian_pacific_islander_pct_officers,
  "ComplianceHold"= crimeData$pct_complaince_hold, "HandFists"= crimeData$pct_hands_fists,"PepperSpray"= crimeData$pct_pepper_spray,"Baton"= crimeData$pct_baton, "LegStrike"= crimeData$pct_leg_strikes,
  "TakeDown"= crimeData$pct_take_down,"DeadlyForce"= crimeData$pct_deadly_force)

demo = colnames(crimeDataMin)[1:8]
for (i in demo){
  crimeDataMin = mutate(crimeDataMin, !!paste0(i,"Quantile") := ntile(crimeDataMin[which(colnames(crimeDataMin)==i)],4))
  as.factor(crimeDataMin[which(colnames(crimeDataMin)==paste0(i,"Quantile"))])
}

crimeData <- crimeDataMin
crimeDataMin <- crimeDataMin[9:23]
crimeDataMin = unnest(crimeDataMin, colnames(crimeDataMin))

crimeDataFilter <- crimeDataMin %>%
  filter(get(paste0("WhiteOfficersQuantile")) %in% c(2) &
           get(paste0("BlackPopulationQuantile")) %in% c(2))

crimeDataOut <- crimeDataMin %>%
  filter(!get(paste0("WhiteOfficersQuantile")) %in% c(2) &
           !get(paste0("BlackPopulationQuantile")) %in% c(2))

#AVERAGING, SD, AND COLLECTING FORCE TYPE INFO
df_forces <- data.frame("ForceTypes" = colnames(crimeDataFilter[1:7]),
                        "overallAverage" = round(as.vector(unlist(lapply(crimeDataMin[1:7], mean))),2),
                        "outsideAverage" =  round(as.vector(unlist(lapply(crimeDataOut[1:7], mean))),2),
                        "filterAverage" = round(as.vector(unlist(lapply(crimeDataFilter[1:7], mean))),2),
                        "overallDeviation" = round(as.vector(unlist(lapply(crimeDataMin[1:7],sd))),2),
                        "outsideDeviaton" =  round(as.vector(unlist(lapply(crimeDataOut[1:7], sd))),2),
                        "filterDeviation" = round(as.vector(unlist(lapply(crimeDataFilter[1:7],sd))),2))

dt_forces = t(df_forces)
dt_forces = setNames(data.frame(t(df_forces[,-1])), df_forces[,1])
row.names(dt_forces) <- c("Average (All Departments)", "Average (Oustide Filter)",
                          "Average (Inside Filter)", "Std. Dev. (All Departments)",
                          "Std. Dev. (Oustide Filter)", "Std. Dev. (Inside Filter)")
#CREATING PLOT
ggplot(data = df_forces,aes(x = ForceTypes)) +
  geom_bar(aes(y = filterAverage),
           stat = "identity",
           fill = "skyblue",
           alpha = 0.8) +
  scale_y_continuous(breaks = seq(0, 100, 10),
                     labels = c("0%", "10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"))+
  geom_errorbar(aes(x = ForceTypes,
                    y = filterAverage,
                    ymin = (filterAverage - filterDeviation),
                    ymax = (filterAverage + filterDeviation)),
                width = 0.2,
                colour = "orange",
                alpha = 0.6,
                size = 1) +
  geom_errorbar(aes(x = ForceTypes,
                    y = overallAverage,
                    ymin = overallAverage,
                    ymax = overallAverage),
                color = "Red",
                lty = 2,
                size = 1) +
  geom_text(aes(y = filterAverage,
                label = paste0(filterAverage, "%"),
                vjust = -1.75)) +
  labs(y = "Frequency (%)",
       x = "Force Used",
       title = "Frequency of Force Used in Police Interactions") +
  theme(plot.title = element_text(hjust = 0.5, size = 16, face = "bold"))


tTestFilterComplianceHold <- t.test(crimeDataFilter$ComplianceHold, crimeDataOut$ComplianceHold)
tTestFilterHandFists <- t.test(crimeDataFilter$HandFists, crimeDataOut$HandFists)
tTestFilterPepperSpray <- t.test(crimeDataFilter$PepperSpray, crimeDataOut$PepperSpray)
tTestFilterBaton <- t.test(crimeDataFilter$Baton, crimeDataOut$Baton)
tTestFilterLegStrike <- t.test(crimeDataFilter$LegStrike, crimeDataOut$LegStrike)
tTestFilterTakeDown <- t.test(crimeDataFilter$TakeDown, crimeDataOut$TakeDown)
tTestFilterDeadlyForce <- t.test(crimeDataFilter$DeadlyForce, crimeDataOut$DeadlyForce)
tTestFilterGroup <- t.test(crimeDataFilter[1:7], crimeDataOut[1:7])

tTestAllComplianceHold <-t.test(crimeDataFilter$ComplianceHold, crimeDataMin$ComplianceHold)
tTestAllHandFists <-t.test(crimeDataFilter$HandFists, crimeDataMin$HandFists)
tTestAllPepperSpray <-t.test(crimeDataFilter$PepperSpray, crimeDataMin$PepperSpray)
tTestAllBaton <-t.test(crimeDataFilter$Baton, crimeDataMin$Baton)
tTestAllLegStrike <-t.test(crimeDataFilter$LegStrike, crimeDataMin$LegStrike)
tTestAllTakeDown <-t.test(crimeDataFilter$TakeDown, crimeDataMin$TakeDown)
tTestAllDeadlyForce <-t.test(crimeDataFilter$DeadlyForce, crimeDataMin$DeadlyForce)
tTestOverallGroup <- t.test(crimeDataFilter[1:7], crimeDataOut[1:7])


forceTypes = unlist(list(colnames(crimeDataFilter[1:7]), "All Force Types"))


df_tTest = data.frame("ForceTypes" = forceTypes,
                 "T Test (Filter vs Overall)" = round(c(tTestAllComplianceHold$p.value, tTestAllHandFists$p.value,
                                                   tTestAllPepperSpray$p.value, tTestAllBaton$p.value,
                                                   tTestAllLegStrike$p.value, tTestAllTakeDown$p.value,
                                                   tTestAllDeadlyForce$p.value, tTestOverallGroup$p.value),3),
                 "T Test (Filter vs Outside)" =round(c(tTestFilterComplianceHold$p.value, tTestFilterHandFists$p.value,
                                                          tTestFilterPepperSpray$p.value, tTestFilterBaton$p.value,
                                                          tTestFilterLegStrike$p.value, tTestFilterTakeDown$p.value,
                                                          tTestFilterDeadlyForce$p.value, tTestFilterGroup$p.value),3))

dt_tTest = t(df_tTest)
dt_tTest = setNames(data.frame(t(df_tTest[,-1])), df_tTest[,1])


chisq.test(crimeDataFilter[1:7], crimeDataOut[1:7])

chisq.test(crimeDataFilter[1:7], crimeDataMin[1:7])

summary(aov(crimeData[,9]  ~ crimeData$WhiteOfficers + crimeData$BlackOfficers + crimeData$AsianPacificOfficers + crimeData$HispanicOfficers+ crimeData$WhitePopulation + crimeData$BlackPopulation + crimeData$AsianPacificPopulation + crimeData$HispanicPopulation))
summary(aov(crimeData[,10] ~ crimeData$WhiteOfficers + crimeData$BlackOfficers + crimeData$AsianPacificOfficers + crimeData$HispanicOfficers+ crimeData$WhitePopulation + crimeData$BlackPopulation + crimeData$AsianPacificPopulation + crimeData$HispanicPopulation))
summary(aov(crimeData[,11] ~ crimeData$WhiteOfficers + crimeData$BlackOfficers + crimeData$AsianPacificOfficers + crimeData$HispanicOfficers+ crimeData$WhitePopulation + crimeData$BlackPopulation + crimeData$AsianPacificPopulation + crimeData$HispanicPopulation))
summary(aov(crimeData[,12] ~ crimeData$WhiteOfficers + crimeData$BlackOfficers + crimeData$AsianPacificOfficers + crimeData$HispanicOfficers+ crimeData$WhitePopulation + crimeData$BlackPopulation + crimeData$AsianPacificPopulation + crimeData$HispanicPopulation))
summary(aov(crimeData[,13] ~ crimeData$WhiteOfficers + crimeData$BlackOfficers + crimeData$AsianPacificOfficers + crimeData$HispanicOfficers+ crimeData$WhitePopulation + crimeData$BlackPopulation + crimeData$AsianPacificPopulation + crimeData$HispanicPopulation))
summary(aov(crimeData[,14] ~ crimeData$WhiteOfficers + crimeData$BlackOfficers + crimeData$AsianPacificOfficers + crimeData$HispanicOfficers+ crimeData$WhitePopulation + crimeData$BlackPopulation + crimeData$AsianPacificPopulation + crimeData$HispanicPopulation))
summary(lm(crimeData[,15] ~ crimeData$WhiteOfficers + crimeData$BlackOfficers + crimeData$AsianPacificOfficers + crimeData$HispanicOfficers+ crimeData$WhitePopulation + crimeData$BlackPopulation + crimeData$AsianPacificPopulation + crimeData$HispanicPopulation))
