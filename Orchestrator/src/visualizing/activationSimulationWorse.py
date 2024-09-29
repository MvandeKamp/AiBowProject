import numpy as np
import matplotlib.pyplot as plt

# Define configurations as dictionaries
configurations = [
    {"bias_init_stdev": 10.0, "weight_init_stdev": 10.0, "activation": "sigmoid", "label": "Sigmoid bias&weight = 10"},
    {"bias_init_stdev": 10.0, "weight_init_stdev": 10.0, "activation": "tanh", "label": "Tanh bias&weight = 10"},
    {"bias_init_stdev": 10.0, "weight_init_stdev": 10.0, "activation": "tanh", "label": "ReLU bias&weight = 10"},
]

# Activation functions
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return np.maximum(x, x)

# Simulate network outputs
def simulate_outputs(config, num_samples=1000):
    biases = np.random.normal(0, config["bias_init_stdev"], num_samples)
    weights = np.random.normal(0, config["weight_init_stdev"], num_samples)
    # Simulate output as a simple linear combination
    raw_outputs = biases + weights

    # Apply activation function
    if config["activation"] == "sigmoid":
        outputs = sigmoid(raw_outputs)
    elif config["activation"] == "tanh":
        outputs = tanh(raw_outputs)
    elif config["activation"] == "relu":
        outputs = relu(raw_outputs)
    else:
        outputs = raw_outputs  # No activation

    return outputs

# Plot the outputs
plt.figure(figsize=(12, 8))
for config in configurations:
    outputs = simulate_outputs(config)
    plt.hist(outputs, bins=50, alpha=0.5, label=f"{config['label']} ({config['activation']})")

# Your plotting code here
plt.title("Output Diversity Across Configurations and Activation Functions")
plt.xlabel("Output Value")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()