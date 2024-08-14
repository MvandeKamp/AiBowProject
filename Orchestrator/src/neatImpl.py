import asyncio
import threading
import time
import datetime


import neat
import math

from ResultList import ResultList
from Stack import Stack
from OutputList import OutputList

inputStack = Stack()
outputList = OutputList()
resultList = ResultList()


# Define the fitness function
async def process_genome(genome_id, genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    global inputStack, outputList, resultList
    while inputStack.size() <= 0:
        await asyncio.sleep(0.5)
    id, x, y, z, workItemId = inputStack.pop()
    aim_at = net.activate((x, y, z))

    # TODO: apply a weight bias if i need to cull the genomes output
    # TODO: a heavy weight bias for wrong bow holding ticks (if its to small the client is not able to fire)
    aim_at = [min(180, max(-180, round(val, 3))) for val in aim_at]
    outputList.append(id, aim_at[0], aim_at[1], aim_at[2], workItemId)
    print(datetime.datetime.now(), f" Client: {id}, Tartget_x: {x}, Target_y: {y}, Target_z: {z} : Aim: {aim_at}")

    # Do a recursion after 60 seconds if no result is given by the client (fail save so the genome is not lost)
    waitTime = time.time()
    while resultList.get(id) is None:
        if(time.time() - waitTime > 60):
            process_genome(genome_id, genome, net)
            return
        await asyncio.sleep(0.5)

    result = resultList.get(id, workItemId)
    print(datetime.datetime.now(), f"Result for Client: {id} Workitem: {workItemId}, result: {result}")
    distance = result[1]
    genome.fitness = 1.0 / (distance + 1.0)
    resultList.remove(id, workItemId)


async def eval_genomes(genomes, config):
    tasks = []
    for genome_id, genome in genomes:
        task = process_genome(genome_id, genome, config)
        tasks.append(task)
    await asyncio.gather(*tasks)


def run_async(genomes, config):
    asyncio.run(eval_genomes(genomes, config))


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
