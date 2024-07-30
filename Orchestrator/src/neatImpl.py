import neat
import math

# Define target position for the fitness function
target_position = (10.0, 5.0, 3.0)

# Define the fitness function
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        inputs = [0.5, 0.5, 0.5]
        arrow_position = net.activate(inputs)
        distance = calculate_distance(arrow_position, target_position)
        genome.fitness = 1.0 / (distance + 1.0)

def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2 + (point2[2] - point1[2]) ** 2)

# Dynamic adjustment function for survival threshold
def adjust_survival_threshold(population, config, generation):
    initial_threshold = 0.1
    final_threshold = 0.5
    max_generations = 1000

    # Linear interpolation between initial and final thresholds
    survival_threshold = initial_threshold + (final_threshold - initial_threshold) * (generation / max_generations)

    # Apply the new survival threshold
    config.reproduction_config.survival_threshold = survival_threshold
    print(f"Generation {generation}: Survival threshold adjusted to {survival_threshold:.2f}")

# Load configuration
config_path = 'neatConfig.ini'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)

# Create population
p = neat.Population(config)

# Add reporters
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)

# Custom run function to integrate dynamic adjustment
def run_neat(config, generations):
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    for generation in range(generations):
        adjust_survival_threshold(population, config, generation)
        population.run(eval_genomes, 1)

    # Get the best genome after all generations
    best_genome = population.best_genome
    return best_genome

# Run the NEAT algorithm with dynamic adjustment
winner = run_neat(config, 1000)

print('\nBest genome:\n{!s}'.format(winner))
