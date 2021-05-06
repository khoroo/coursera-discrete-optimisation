#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
from ortools.sat.python import cp_model

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        u, v = map(int, line.split())
        edges.append((u, v))


    model = cp_model.CpModel()

    nodes = [model.NewIntVar(0, node_count, f'node_{i}') for i in range(node_count)]
    max_color = model.NewIntVar(0, node_count, 'max_color')
    model.AddMaxEquality(max_color, nodes)


    for e in edges:
        model.Add(nodes[e[0]] != nodes[e[1]])

    for i in range(node_count):
        model.Add(nodes[i] <= i+1)


    model.Minimize(max_color)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 4
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        opt = 1
        colors = [solver.Value(n) for n in nodes]
        obj = solver.Value(max_color) + 1
    else:
        opt = 0
        colors = range(node_count)
        obj = node_count


    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(opt) + '\n'
    output_data += ' '.join(map(str, colors))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

