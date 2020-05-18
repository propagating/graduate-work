# Title     : Iris Analysis
# Objective : CS629-2 Iris Assignment
# Created by: Ryan Richardson
# Created on: 16/05/2020

library(datasets)
library(dplyr)
library(magrittr)
library(ggplot2)


data(iris)
data(co2)

summary(iris)
names(iris) <- tolower(names(iris))
virginica <- filter(iris, iris$species == "virginica")
setosa <- filter(iris, iris$species == "setosa")
versicolor <- filter(iris, iris$species == "versicolor")

#versicolor only
ggplot(iris, aes(sepal.length, sepal.width)) + geom_point(aes(color=species))+ scale_color_manual(name="Species", values=c("black", "red", "black"))
ggplot(iris, aes(sepal.length, sepal.width)) + geom_point(aes(size=species))+ scale_size_manual(name="Species", values=c(1, 4, 1))
ggplot(iris, aes(sepal.length, sepal.width)) + geom_point(aes(shape=species))+ scale_shape_manual(name="Species", values=c(0,4,0))

#joint graphs
ggplot(iris, aes(sepal.length, sepal.width)) + geom_point(aes(color=species, shape=species))
ggplot(iris, aes(sepal.length, sepal.width)) + geom_point(aes(size=species, color=species, shape=species))



#co2 data
#Concentration and uptake are integrable, while Treatment and Type are separable. Separable variablces can be encoded using
#color and shape in this case, while itegrable data can be plotted normally
summary(CO2)
ggplot(co, aes(uptake, conc)) + geom_point(aes(shape=Type, color=Treatment)) +
  scale_color_manual(name="Treatment", values=c("#33FFFF", "#330066")) +
  scale_shape_manual(name="Location", values=c(16,22))