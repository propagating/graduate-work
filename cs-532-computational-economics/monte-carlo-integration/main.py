import random
import numpy as np
count = 0
for i in range(10000):
    x = random.random()
    y = random.random()
    if y <= x**3:
        count += 1

def f_area_random(num_trials):
    count =0
    for i in range(num_trials):
        x = random.random()
        count+= x**3 >= random.random()
    return count/num_trials

n = 10000
num_trials = 100
value_list = [f_area_random(num_trials) for _ in range(n)]
print(f"Approx. Area:\t{np.mean(value_list):.2f}")
print(f"Variance: {np.var(value_list):.4f}")

def f_area_antithetic(num_trials):
    count =0
    for i in range(num_trials//2):
        x = random.random()
        antithetic = 1-x
        count += x**3 >= random.random()
        count += antithetic**3 >= random.random()
    return count/num_trials

value_list = [f_area_antithetic(num_trials) for _ in range(n)]
print(f"Approx. Area:\t{np.mean(value_list):.4f}")
print(f"Variance: {np.var(value_list):.4f}")