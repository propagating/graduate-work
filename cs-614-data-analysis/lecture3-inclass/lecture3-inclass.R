
gdp <- read.csv('data/gdp.csv')
cca <- read.csv('data/countrycharsA.csv')
ccb <- read.csv('data/countrycharsB.csv')

str(gdp)
str(cca)
str(ccb)

ccs <- rbind(cca, ccb)
ccgs <- cbind(ccs, gdp)

str(gdp)
str(cca)
str(ccs)
str(ccgs) # country is a a chr datatype, denoting a c-style string/array of characters


aboveThreshold = ccgs[which(ccgs$year > 1980 & ccgs$gdp < 20000),]
str(aboveThreshold) # 687  above the threshold


medianByYear = data.frame("Year" = c(), "MedianGdp" = c(), "ClosestRelativeGdp" = c())
for (i in unique(ccgs$year)) {
  
  yearResults = ccgs[which(ccgs$year == i),] 
  
  gdpMedian = median(yearResults$gdp)
  gdpDifference = abs(yearResults$gdp - gdpMedian)
  
  minCountry = yearResults[which.min(gdpDifference),]
  medianByYear = rbind(medianByYear, list(i, gdpMedian, minCountry$country))
  
}

str(medianByYear)

medianByYearByContinent = data.frame("Year" = c(), "MedianGdp" =  c(), "ClosestRelativeGdp" = c(), "Continent" = c())
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

str(medianByYearByContinent)