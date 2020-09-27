gdp <- read.csv('data/gdp.csv')
cca <- read.csv('data/countrycharsA.csv')
ccb <- read.csv('data/countrycharsB.csv')
ccs <- rbind(cca, ccb)
ccgs <- cbind(ccs, gdp)


medianByYear = data.frame("Year" = c(), "MedianGdp" = c(), "ClosestRelativeGdp" = c())
medianByYearByContinent = data.frame("Year" = c(), "MedianGdp" =  c(), "ClosestRelativeGdp" = c(), "Continent" = c())


for (i in unique(ccgs$year)) {
  
  yearResults = ccgs[which(ccgs$year == i),] 
  
  gdpMedian = median(yearResults$gdp)
  gdpDifference = abs(yearResults$gdp - gdpMedian)
  
  minCountry = yearResults[which.min(gdpDifference),]
  medianByYear = rbind(medianByYear, list(i, gdpMedian, minCountry$country))
  
}


for (i in unique(ccgs$year)) {
  
  yearResults = ccgs[which(ccgs$year == i),] 
  
  for (j in unique(yearResults$continent)) {
    
    continentResults = yearResults[which(yearResults$continent == j),]
    
    gdpMedian = median(continentResults$gdp)
    gdpDifference = abs(continentResults$gdp - gdpMedian)
    
    minCountry = continentResults[which.min(gdpDifference),]
    medianByYearByContinent = rbind(medianByYearByContinent, list(i, gdpMedian, minCountry$country, minCountry$continent))
    
  }
  
}

load("data/map.coords.RData")
coords <- coords # R getting mad that coords didn't exist despite being loaded unless it was re-cast to var

leftJoin <- merge(x = ccgs, y = coords, by = "country", all.x = TRUE) 
# 1667 by 8, 2 new cols added. 
# Number of obersevations would always need to be at least the same as the number of rows in our first dataframe. 
# If there were missing values on the merge then those values are l
# left empty in the joined set.

rightJoin <- merge(x = ccgs, y = coords, by = "country", all.y = TRUE) 
# 1657 by 8, 2 new cols but missing 10 records because the coords dataset's country col
# does not have a match for those 10 records. There may still be rows with empty values 
# if they were present in the original coords dataset but not the ccgs dataset

innerJoin <-  merge(x = ccgs, y = coords, by = "country")
# 1535 by 8, 2 new cols. Only data matched in both sets are included here, 
# anything that was unable to find a succesfull match is excluded form the joined set. 


