import random

# Generate 1000 random numbers between 0.8 and 1.6 with one decimal place
random_numbers = [round(random.uniform(0.8, 1.6), 1) for _ in range(1000)]

# Print the first 10 generated numbers
print(random_numbers[:10])

