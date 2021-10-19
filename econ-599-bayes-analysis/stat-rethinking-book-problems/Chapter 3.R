library(HDInterval)
library(ggpmisc)
p_grid <- seq( from=0 , to=1 , length.out=1000 )
prior <- rep( 1 , 1000 )
likelihood <- dbinom( 6 , size=9 , prob=p_grid )
posterior <- likelihood * prior
posterior <- posterior / sum(posterior)
set.seed(100)
samples <- sample( p_grid , prob=posterior , size=1e4 , replace=TRUE )

one <- sum(samples < 0.2)/length(samples)
two <- sum(samples > 0.8)/length(samples)
three <- sum( samples < 0.8 & samples > 0.2)/length(samples)
four <- quantile(samples, 0.2)
five <- quantile(samples, 0.8)
six <- hdi(samples, credMass = 0.66)
seven <- quantile(samples, probs=c(1/6, 5/6))


birth1 <- c(1,0,0,0,1,1,0,1,0,1,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,0,
            0,0,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,
            1,1,0,1,0,0,1,0,0,0,1,0,0,1,1,1,1,0,1,0,1,1,1,1,1,0,0,1,0,1,1,0,
            1,0,1,1,1,0,1,1,1,1)
birth2 <- c(0,1,0,1,0,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,0,
            1,1,1,0,1,1,1,0,1,0,0,1,1,1,1,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,
            1,1,1,0,1,1,0,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,0,0,1,1,
            0,0,0,1,1,1,0,0,0,0)

totalBoys = sum(birth1) + sum(birth2)
birthPrior <- 1
birthLikelihood <- dbinom(totalBoys, length(birth1) + length(birth2),p_grid)
birthPosterior <- birthPrior*birthLikelihood
birthPosteriorNorm <- birthPosterior/sum(birthPosterior)
plot(p_grid, birthPosteriorNorm)
birthMaxProbability <- p_grid[which.max(birthPosteriorNorm)]
h1 <- birthMaxProbability

birthPostSample = sample(p_grid, prob = birthPosterior, replace=TRUE, size = 10000)
h2a <- hdi(birthPostSample, credMass = 0.5)
h2b <- hdi(birthPostSample, credMass = 0.89)
h2c <- hdi(birthPostSample, credMass = 0.97)

birthRandomSample <-rbinom(10000, size = 200, prob=birthPostSample)

hist(birthRandomSample)


birthRandomSample100 <-rbinom(10000, size = 100, prob=birthPostSample)
hist(birthRandomSample100)

birthGirls = sum(birth2[birth1== 0])
birthBoys = sum(birth2[birth1 == 0])
