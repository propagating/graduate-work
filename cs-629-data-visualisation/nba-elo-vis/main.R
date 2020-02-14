# Title     : NBA ELO Outcomes
# Objective : Determine win chance and point difference by team ELO
# Created by: Ryan Richardson, Riley Kendall
# Created on: 2/9/2020
library(ggplot2)
library(dplyr)

nbaData = read.csv("Data\\nbaelo.csv",TRUE)
noCopies = nbaData[!(nbaData$X_iscopy == 0),]

noCopies$game_result = as.factor(noCopies$game_result)

p<- ggplot(noCopies, aes(x=game_result, y=elo_i, fill=game_result)) +
  geom_violin(trim=FALSE) +
  geom_boxplot(width=0.1, fill="white") +
  labs(title = "Starting ELO vs Game Result", x="Game Result", y="ELO Rating") +
  scale_fill_brewer(palette = "Blues") +
  theme_classic()

eloDiff = noCopies$elo_i - noCopies$opp_elo_i
ptsDiff = noCopies$pts - noCopies$opp_pts

pt <- qplot(ptsDiff, eloDiff, data=noCopies, color=as.factor(game_result)) +
  geom_smooth(aes(group=game_result), color="black")+
  labs(title="ELO Difference vs Point Difference", x="Point Difference",y="ELO Difference", colour="Game Result")


# this graph is meaningless, forecast is an elo based win rate to begin with, so there is a guaranteed correlation
# a proper comparison would look at a time period accuracy between a teams forecast and their current win percentage by season
tt <- qplot(forecast, elo_i, data=noCopies, color= as.factor(game_result)) +
  geom_smooth(color="black")+
  labs(title="Team ELO", x="Forceasted Win Rate",y="ELO Differnce ", colour="Game Result")

nbaData$date_game = as.Date(nbaData$date_game, format = "%m/%d/%y")
convertedLosses = nbaData$game_result <- as.numeric(nbaData$game_result) - 1
#winsByTeam = aggregate(convertedLosses, by=list(Team = nbaData$team_id), FUN = mean)