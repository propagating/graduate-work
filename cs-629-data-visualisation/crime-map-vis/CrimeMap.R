# Color for Maps 
library(ggplot2)
library(reshape2)
library(dplyr) # required for arrange()
library(colorspace)
library(viridis)
library(maps) # for the state map data


# required packages

states_map <- map_data("state") #extracts data from the states map

# Make a data set of US crime data from the USArrests data set
crimes <- data.frame(state = tolower(rownames(USArrests)), USArrests)
crimes$Arrests = crimes$Murder + crimes$Assault + crimes$Rape
crime_map <- merge(states_map, crimes, by.x = "region", by.y = "state")
crime_map <- arrange(crime_map, group, order)
head(crime_map)


# Color map diverging from the midpoint (mean murder rate) with colorspace 
basemap <- ggplot(crime_map, aes(x = long, y = lat, group = group, fill = Murder, alpha = Arrests)) +
    geom_polygon() + coord_map("polyconic") + scale_fill_continuous_diverging(palette = "Blue-Red", mid = mean(crime_map$Murder))

basemap