import asyncio
import os
import threading
import time
import datetime

import neat
import math

from ResultList import ResultList
from Stack import Stack
from OutputList import OutputList

import logging
from logging.handlers import TimedRotatingFileHandler

# Configure logging
logger = logging.getLogger('genome_logger')
logger.setLevel(logging.INFO)

# Create a handler that writes log messages to a file, rotating every 5 minutes
handler = TimedRotatingFileHandler('genome_process.log', when='M', interval=5, backupCount=500)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

inputStack = Stack()
outputList = OutputList()
resultList = ResultList()


async def process_genome(genome_id, genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    global inputStack, outputList, resultList

    while True:
        while inputStack.size() <= 0:
            await asyncio.sleep(0.5)

        id, x, y, z, workItemId = await inputStack.pop()
        aim_at = net.activate((x, y, z))

        # Scale the outputs to the range of -180 to 180
        aim_at = [val * 180 for val in aim_at]

        aim_at = (aim_at[0], aim_at[1], 20)
        if aim_at[2] < 15:
            aim_at[2] = 15

        # Ensure the values are within the specified range and round them
        aim_at = [min(180, max(-180, round(val, 3))) for val in aim_at]
        outputList.append(id, aim_at[0], aim_at[1], aim_at[2], workItemId)

        logger.info(
            f"Stack size: {inputStack.size()}, Output list size: {outputList.size()}, Result list size: {resultList.size()}")
        logger.info(f"Client: {id}, Workitem: {workItemId}, Target_x: {x}, Target_y: {y}, Target_z: {z} : Aim: {aim_at}")
        print(f"Client: {id}, Workitem: {workItemId}, Target_x: {x}, Target_y: {y}, Target_z: {z} : Aim: {aim_at}")

        waitTime = time.time()
        while resultList.get(id, workItemId) is None:
            if (time.time() - waitTime > 60):
                # Instead of recursion, break and retry the loop
                if outputList.get(id, workItemId) is not None:
                    outputList.remove(id, workItemId)
                logger.warning(f"Client {id} did not respond reqeuing genome!")
                print(f"Client {id} did not respond reqeuing genome!")
                break
            await asyncio.sleep(0.5)
        else:
            # If result is found, process it
            result = resultList.get(id, workItemId)
            logger.info(f"Result for Client: {id} Workitem: {workItemId}, result: {result}")
            print(f"Result for Client: {id} Workitem: {workItemId}, result: {result}")
            distance = result[1]
            genome.fitness = (1.0 / (distance + 1.0))
            resultList.remove(id, workItemId)
            return


async def eval_genomes(genomes, config):
    tasks = []
    for genome_id, genome in genomes:
        task = process_genome(genome_id, genome, config)
        tasks.append(task)
    await asyncio.gather(*tasks)


def run_async(genomes, config):
    asyncio.run(eval_genomes(genomes, config))

# Dynamic adjustment function for survival threshold
def adjust_survival_threshold(population, config, generation):
    initial_threshold = 0.1
    final_threshold = 0.8
    maxgen = 1000
    # Linear interpolation between initial and final thresholds
    #survival_threshold = initial_threshold + (final_threshold - initial_threshold) * (generation / maxgen)
    survival_threshold = 0.2
    # Apply the new survival threshold
    config.reproduction_config.survival_threshold = survival_threshold
    print(f"Generation {generation}: Survival threshold adjusted to {survival_threshold:.2f}")


import sys

sys.path.insert(0, 'Orchestrator/src/neatConfig.ini')
# Load configuration
config_path = 'Orchestrator/src/neatConfig.ini'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)

max_generations = 5000
def run():
    winner = run_neat(config, max_generations)
    print('\nBest genome:\n{!s}'.format(winner))


def run_neat(config, generations):
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats_reporter = neat.StatisticsReporter()
    population.add_reporter(stats_reporter)

    for generation in range(generations):
        adjust_survival_threshold(population, config, generation)
        population.run(run_async, 1)

        # Get the best genome of the current generation
        best_genome = stats_reporter.best_genomes(1)

        # Log the best genome
        logger.info(f"Best genome in Generation {generation}: {best_genome}")
        logger.info(f"Generation {generation} Mean: {stats_reporter.get_fitness_mean()} STDev: {stats_reporter.get_fitness_stdev()}")

        # Save the best genome to a file
        save_best_genome(best_genome, generation)

    # Get the best genome after all generations
    best_genome = population.best_genome
    logger.info(f"Best genome after all generations: {best_genome}")
    return best_genome


def save_best_genome(genome, generation):
    # Create a directory to save genomes if it doesn't exist
    if not os.path.exists('best_genomes'):
        os.makedirs('best_genomes')

    # Save the genome to a file
    file_path = f'best_genomes/best_genome_gen_{generation}.pkl'
    with open(file_path, 'wb') as f:
        import pickle
        pickle.dump(genome, f)

    print(f"Best genome of generation {generation} saved to {file_path}")
