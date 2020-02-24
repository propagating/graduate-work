# Title     : Bauhaus Color Wheel
# Objective : Create a Segmented Bauhaus Color Wheel
# Created by: Ryan
# Created on: 2/23/2020

### READ READ READ ###
# install color mod using dev tools. UNCOMMENT IF NEEDED
#if(!require("devtools")) install.packages("devtools")
#devtools::install_github("briandconnelly/colormod")

library(circlize)
library(colormod)
library(colorspace)


color_pattern = c("#994F50","#994F50", "#B12D20","#B12D20", "#CE2F19","#CE2F19", "#E34F11", "#E34F11",
                  "#F7B008","#F7B008", "#FCD905","#FCD905","#EEC920", "#EEC920","#478C70", "#478C70",
                  "#00487A","#00487A", "#043871","#043871", "#073A73","#073A73", "#374373", "#374373")

color_pattern = adjust_hsv(color_pattern, s=.3, v=-.3)
color_pattern = darken(color_pattern, amount = 0.25)


factors = 1:length(color_pattern)

circos.par(gap.degree = 0, cell.padding = c(0, 0, 0, 0),
           start.degree = 90, track.margin = c(0, 0), clock.wise = TRUE)
circos.initialize(factors = factors, xlim = c(0, 1))
circos.clear

hsv_changes = 1:(length(color_pattern)*.5)

for (i in hsv_changes){
  circos.track(ylim = c(0, 1), factors = factors,
               bg.col = color_pattern, bg.border = "black", track.height = 0.15)
  color_pattern = adjust_hsv(color_pattern, s=-(.15), v=+(.15))
  color_pattern = lighten(color_pattern, amount =.18/length(hsv_changes))
}

start.degree = 30
end.degree = 0
divs = 1:(length(color_pattern)*.5)
for (i in divs){
  draw.sector(center = c(0, 0), start.degree, end.degree,
              rou1 = 0.1, col = "white", border = "black")
  start.degree = (start.degree + 30)
  end.degree = (end.degree + 30)
}

