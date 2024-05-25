# 3D Traveling Salesman Problem Solver using Genetic Algorithm

This repository contains a Python implementation to solve the 3D Traveling Salesman Problem (TSP) using Genetic Algorithm (GA).

## Input and Output

The input should be provided in a file named `input.txt`, which is formatted as follows:
- The first line contains a strictly positive 32-bit integer `N`, indicating the number of city locations in the 3D space.
- The next `N` lines each contain three non-negative 32-bit integers separated by a space, representing the coordinates (x, y, z) of each city.

The output should be:
- The first line contains the total distance of the path.
- The next `N+1` lines contain the coordinates of the cities visited in order, starting and ending at the same city.

## Genetic Algorithm Approach
-Initialization: Generate an initial population of possible solutions (tours).
-Selection: Select pairs of solutions from the current population to breed based on their fitness.
-Crossover: Combine pairs of solutions to produce offspring solutions.
-Mutation: Apply random changes to individual solutions to maintain genetic diversity.
-Evaluation: Calculate the fitness of each solution based on the total distance of the tour.
-Iteration: Repeat the selection, crossover, mutation, and evaluation steps until a stopping criterion is met (e.g., a fixed number of generations or a satisfactory fitness level).
