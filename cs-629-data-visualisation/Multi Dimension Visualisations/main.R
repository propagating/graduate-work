# Title     : TODO
# Objective : TODO
# Created by: Ryan
# Created on: 3/18/2020

library(rayshader)
library(ggplot2)
library(tidyverse)
library(viridis)
library(rgdal)

gg = ggplot(diamonds, aes(x, depth)) +
  stat_density_2d(aes(fill = stat(nlevel)),
                  geom = "polygon",
                  n = 100,bins = 10,contour = TRUE) +
  facet_wrap(clarity~.) +
  scale_fill_viridis_c(option = "A")
gg
plot_gg(gg,multicore=TRUE,width=5,height=5,scale=250)