import numpy as np
from scipy.spatial import distance
import pygame
import random

#returns the individual from population with the lowest fitness
def select_incumbent(fitness, population):
    inc_fit = fitness[0]
    inc = population[0]
    for i in range(0, len(population)):
        if fitness[i] < inc_fit:
            inc_fit = fitness[i]
            inc = population[i]
    return inc, inc_fit

#selects an individual from the population based on 3-ary tournament selection
def select_tournament(fitness):
    cand1 = random.randint(0, len(fitness)-1)
    cand2 = random.randint(0, len(fitness)-1)
    cand3 = random.randint(0, len(fitness)-1)
    f = cand1
    if fitness[cand2] < fitness[f]:
        f = cand2
    if fitness[cand3] < fitness[f]:
        f = cand3
    return f

#create offspring from parent1 and 2 with order 1 crossover
def order_crossover(parent1, parent2):
    child = parent1[:int(len(parent1)/2)]
    rest = []
    for i in parent2:
        if not (i in child):
            rest.append(i)
    child = np.append(child, rest)
    return child


class GA:
    def __init__(self, cities, city_count, draw_route, mu, pc, pm):
        self.idle_count = 0
        self.cities = cities
        self.city_count = city_count
        self.draw_route = draw_route
        self.equal_count = 0
        self.mu = mu #population size
        self.pc = pc #crossover rate
        self.pm = pm  #permutation rate

        #initalize population and fitness
        self.population = []
        self.fitness = []

        for i in range(0, self.mu):
            self.population.append(np.random.permutation(city_count))
        for i in range(0, self.mu):
            self.fitness.append(self.calc_fitness(self.population[i]))

        self.inc, self.inc_fitness = select_incumbent(self.fitness, self.population)
        print("Fitness of initial incumbent:", self.inc_fitness)
        self.draw_route(self.inc)

    #returns the fitness of individual = the total euclidean distance of the travel between all cities
    def calc_fitness(self, individual):
        fitness = 0
        for i in range(0, len(individual)-1):
            point1 = self.cities[individual[i]]
            point2 = self.cities[individual[i+1]]
            fitness += distance.euclidean(point1, point2)
        return fitness

    def incumbent(self):
        print("Final incumbent:", self.inc, "with fitness:", self.inc_fitness)

    #single iteration of the Genetic Algorithm (GA)
    def optimize(self):
            pygame.event.pump() #prevent OS from thinking pygame has crashed

            new_population = []
            new_fitness = []
            for i in range(0, self.mu):
                p1 = select_tournament(self.fitness)
                p1_genome = self.population[p1]
                c_genome = p1_genome

                if random.uniform(0, 1) < self.pc: #crossover
                    p2 = p1
                    while p2 == p1:
                        p2 = select_tournament(self.fitness)
                    p2_genome = self.population[p2]

                    c_genome = order_crossover(p1_genome, p2_genome)

                for i in range(0, self.city_count): #mutation
                    if random.uniform(0, 1) < self.pm:
                        j = random.randint(0, self.city_count-1)
                        c_genome[i], c_genome[j] = c_genome[j], c_genome[i]

                new_population.append(c_genome)
                new_fitness.append(self.calc_fitness(c_genome))

            self.population = new_population
            self.fitness = new_fitness

            inc, inc_fitness = select_incumbent(self.fitness, self.population)
            if inc_fitness < self.inc_fitness:
                self.inc, self.inc_fitness = inc, inc_fitness
                print("Fitness of current incumbent:", self.inc_fitness)
                self.draw_route(self.inc)
            else:
                self.equal_count += 1