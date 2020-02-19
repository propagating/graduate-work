library(ggplot2)
library(reshape)

meltedData = melt(volcano)
vpltColour <- ggplot(aes(x = 'X1', y = 'X2'), data = meltedVolcano) + geom_tile(aes(fill = value), data = meltedVolcano)
vpltColour

vpltGray <- ggplot(meltedVolcano, aes(x = X1, y = X2)) + geom_tile(aes(fill = value)) + scale_fill_gradient(low = 'gray10', high = 'gray80')
vpltGray

vpltContour <- ggplot(meltedVolcano, aes(x = X1, y = X2, z = value)) + geom_tile(aes(fill = value)) + geom_contour(colour = 'white') + scale_fill_gradient(low = 'gray10', high = 'gray80')
vpltContour