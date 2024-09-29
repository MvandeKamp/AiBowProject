import os
import re
import matplotlib.pyplot as plt

def process_log_file(file_path):
    best_result = float('inf')

    with open(file_path, 'r') as file:
        for line in file:
            # Match lines with the result information
            match = re.search(r"result: \('.*?', ([\d.]+),", line)
            if match:
                result_value = float(match.group(1))
                if result_value < best_result:
                    best_result = result_value

    if best_result < float('inf'):
        fitness = 1 / (best_result + 1)
        return fitness
    else:
        return None

def process_log_folder(folder_path):
    fitness_values = []
    generation_numbers = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and not file_name.startswith('.'):
            print(f"Processing file: {file_name}")
            fitness = process_log_file(file_path)
            if fitness is not None:
                generation_number = extract_generation_number(file_name)
                fitness_values.append(fitness)
                generation_numbers.append(generation_number)

    return generation_numbers, fitness_values

def extract_generation_number(file_name):
    # Assuming the generation number is part of the file name, e.g., "generation_108"
    match = re.search(r"generation_(\d+)", file_name)
    if match:
        return int(match.group(1))
    else:
        return len(file_name)  # Fallback if no generation number is found

def plot_fitness(generation_numbers, fitness_values):
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_values, marker='o', linestyle='-')
    plt.ylabel('Fitness')
    plt.xlabel('Generation')
    plt.title('Bestes Genome pro Generation')
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# Specify the path to the folder containing the log files
log_folder_path = 'logs'
generation_numbers, fitness_values = process_log_folder(log_folder_path)
plot_fitness(generation_numbers, fitness_values)