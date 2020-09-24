import random
import numpy as np


def unfiformSampling(trialCount):
    uniformCount = 0
    for i in range(trialCount):
        ux = random.random()
        uy = random.random()
        if uy <= ux ** 3:
            uniformCount += 1
    return uniformCount / trialCount


def antitheticSampling(trialCount):
    antitheticCount = 0
    for i in range(trialCount // 2):
        x = random.random()
        ax = 1 - x
        uy = random.random()
        if uy <= ax ** 3:
            antitheticCount += 1
        if uy <= x ** 3:
            antitheticCount += 1
    return antitheticCount / trialCount


simRounds = 100000
trials = 100
uniformSamplingValues = [unfiformSampling(trials) for _ in range(simRounds)]
print(f"Uniform Sampling Area Mean:\t{np.mean(uniformSamplingValues):.4f}")
print(f"Uniform Sampling Area Variance: {np.var(uniformSamplingValues):.4f}")


antitheticSamplingValues = [antitheticSampling(trials) for _ in range(simRounds)]
print(f"Antithetic Sampling Area Mean:\t{np.mean(antitheticSamplingValues):.4f}")
print(f"Antithetic Sampling Area Variance: {np.var(antitheticSamplingValues):.4f}")