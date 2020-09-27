qplot(time, temp, + colour = activ, + facets = activ ~ ., + geom = c("point", "smooth"), data = second) + +theme_bw(base_size = 12, base_family = "")

qplot(time, temp,colour = activ,facets = activ ~ .,geom = c("point", "smooth"), data = first) +theme_bw(base_size = 12, base_family = "")
