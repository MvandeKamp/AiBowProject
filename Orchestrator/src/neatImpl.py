import asyncio
import threading
import time

import neat
import math

from ResultList import ResultList
from Stack import Stack
from OutputList import OutputList

# Define target position for the fitness function
target_position = (10.0, 5.0, 3.0)
inputStack = Stack()
outputList = OutputList()
resultList = ResultList()


# Define the fitness function
async def process_genome(genome_id, genome, config, inputStack, outputList, resultList):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    if not inputStack.size() > 0:
        await asyncio.sleep(0.5)
    id, x, y, z = inputStack.pop()
    aim_at = net.activate((x, y, z))
    outputList.append(id, aim_at[0], aim_at[1], aim_at[2], aim_at[3])
    result = resultList.get(id)
    if result is None:
        await asyncio.sleep(0.5)
    distance = result[1]
    genome.fitness = 1.0 / (distance + 1.0)


async def eval_genomes(genomes, config, inputStack, outputList, resultList):
    tasks = []
    for genome_id, genome in genomes:
        task = process_genome(genome_id, genome, config, inputStack, outputList, resultList)
        tasks.append(task)
    await asyncio.gather(*tasks)


def run_async(genomes, config):
    asyncio.run(eval_genomes(genomes, config, inputStack, outputList, resultList))


def calculate_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2 + (point2[2] - point1[2]) ** 2)


# Dynamic adjustment function for survival threshold
def adjust_survival_threshold(population, config, generation):
    initial_threshold = 0.1
    final_threshold = 0.5
    max_generations = 100

    # Linear interpolation between initial and final thresholds
    survival_threshold = initial_threshold + (final_threshold - initial_threshold) * (generation / max_generations)

    # Apply the new survival threshold
    config.reproduction_config.survival_threshold = survival_threshold
    print(f"Generation {generation}: Survival threshold adjusted to {survival_threshold:.2f}")

import sys
sys.path.insert(0,'Orchestrator/src/neatConfig.ini')
# Load configuration
config_path = 'Orchestrator/src/neatConfig.ini'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)

# Create population
p = neat.Population(config)

# Add reporters
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)


def run():
    winner = run_neat(config, 100)
    print('\nBest genome:\n{!s}'.format(winner))


# Custom run function to integrate dynamic adjustment
def run_neat(config, generations):
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    for generation in range(generations):
        adjust_survival_threshold(population, config, generation)
        population.run(run_async, 1)

    # Get the best genome after all generations
    best_genome = population.best_genome
    return best_genome
