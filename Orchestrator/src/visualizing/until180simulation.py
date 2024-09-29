import random
import matplotlib.pyplot as plt
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def simulate(weight, bias, target):
    total = 0
    tries = 0
    while total < target:
        # Calculate the probability using the sigmoid function
        probability = sigmoid(weight + bias)
        # Simulate a coin flip with the calculated probability
        if random.random() < probability:
            total += weight + bias
        tries += 1
    return tries

def main():
    weight = 10  # Example weight
    bias = 5     # Example bias
    target = 180
    num_simulations = 1000
    results = []

    for _ in range(num_simulations):
        tries = simulate(weight, bias, target)
        results.append(tries)

    # Plotting the results
    plt.hist(results, bins=30, edgecolor='black')
    plt.title('Distribution of Tries to Reach 180')
    plt.xlabel('Number of Tries')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    main()