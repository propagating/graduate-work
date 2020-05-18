library(rayshader)
library(ggplot2)
library(rlang)
library(viridis)
library(rayshader)
install.packages('rgdal')

#Here, I load a map with the raster package.
loadzip = tempfile() 
download.file("https://tylermw.com/data/dem_01.tif.zip", loadzip)
localtif = raster::raster(unzip(loadzip, "dem_01.tif"))
unlink(loadzip)

#And convert it to a matrix:
elmat = raster_to_matrix(localtif)

#We use another one of rayshader's built-in textures:
elmat %>%
  sphere_shade(texture = "desert", sunangle=15) %>%
  add_water(detect_water(elmat), color = "desert") %>%
  add_shadow(ray_shade(elmat), 0.2) %>%
  add_shadow(ambient_shade(elmat), 0.1) %>%
  plot_3d(elmat, zscale = 10, fov = 0, theta = 135, zoom = 0.75, phi = 45, windowsize = c(1000, 800))

#sets ranges for axis movement 
thetavec = 360 + 15 * sin(seq(0,359,length.out = 360) * pi/180)
phivec = 20 + 70 * 1/(1 + exp(seq(-5, 10, length.out = 180)))
zoomvechalf = .2 + 0.5 * 1/(1 + exp(seq(-10, 10, length.out = 180)))
zoomvec = c(zoomvechalf, rev(zoomvechalf))
phivecfull = c(phivec, rev(phivec))


render_movie(filename="rayshade.mp4", type="custom", theta = thetavec,  
             phi=phivecfull, zoom=zoomvec, fov=0)