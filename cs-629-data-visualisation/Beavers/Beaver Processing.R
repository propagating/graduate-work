# Beaver Processing
b1 = beaver1
b2 = beaver2

# changes time to be more meaningful measure of how many hours since start of mesaurement
b1$hours <- b1$time %/% 100 + 24 * (b1$day - b1$day[1]) + (b1$time %% 100) / 60
b2$hours <- b2$time %/% 100 + 24 * (b2$day - b2$day[1]) + (b2$time %% 100) / 60

# identifies beaver prior to appending data
b1$beaver = 1
b2$beaver = 2

# converts day to factor for easier comparisons
b1$day = factor(b1$day, labels = c("Day 1", "Day 2"))
b2$day = factor(b2$day, labels = c("Day 1", "Day 2"))

# combines into single beaver dataframe and makes beaver a factor
beavers = rbind(b1, b2)
beavers$beaver = factor(beavers$beaver)

# prints beaver head
head(beavers)