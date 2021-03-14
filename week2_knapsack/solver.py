#!/usr/bin/python
# -*- coding: utf-8 -*-

from ortools.algorithms import pywrapknapsack_solver

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = [int(firstLine[1])]

    values = []
    weights = [[]]

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        values.append(int(parts[0]))
        weights[0].append(int(parts[1]))

    # from the or-tools knaspack example
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    solver.Init(values, weights, capacity)
    computed_value = solver.Solve()
    taken = [0 for _ in range(item_count)]
    total_weight = 0
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            taken[i] = 1
            total_weight += weights[0][i]


    output_data = str(computed_value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    # 0 0 1 0
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

